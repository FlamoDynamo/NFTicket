from pyteal import *
import json

def approval_program():
    MAX_EVENTS = Int(5)
    MAX_ATTENDANTS = Int(100)  # Giới hạn số người tham gia là 100 người
    EVENT_COUNT = Bytes("event_count")
    EVENT_NFT_PREFIX = Bytes("event_")
    NFT_ID_SUFFIX = Bytes("_nft_id")
    EVENT_END_PREFIX = Bytes("event_end_")
    EVENT_STOPPED_PREFIX = Bytes("event_stopped_")
    EVENT_ATTENDANTS_PREFIX = Bytes("event_attendants_")
    EVENT_TICKET_COUNT_PREFIX = Bytes("event_ticket_count_")
    EVENT_TICKET_ISSUED_PREFIX = Bytes("event_ticket_issued_")
    TICKET_CODE_PREFIX = Bytes("ticket_code_")  # Mã vé cho từng người tham dự
    CURRENT_TICKET_CODE = Bytes("current_ticket_code")  # Mã vé hiện tại, tăng dần

    def int_to_str(i):
        return If(
            i == Int(1),
            Bytes("1"),
            If(
                i == Int(2),
                Bytes("2"),
                If(
                    i == Int(3),
                    Bytes("3"),
                    If(
                        i == Int(4),
                        Bytes("4"),
                        If(
                            i == Int(5),
                            Bytes("5"),
                            Bytes("")  # Fallback, should not happen due to MAX_EVENTS
                        )
                    )
                )
            )
        )

    on_creation = Seq([
        App.globalPut(EVENT_COUNT, Int(0)),
        App.globalPut(CURRENT_TICKET_CODE, Int(1)),  # Khởi tạo mã vé hiện tại là 1
        Return(Int(1))
    ])

    create_event = And(
        Txn.application_args.length() == Int(4),
        Txn.application_args[0] == Bytes("create_event"),
        Txn.sender() == Global.creator_address()
    )

    handle_create_event = Seq([
        Assert(App.globalGet(EVENT_COUNT) < MAX_EVENTS),
        App.globalPut(EVENT_COUNT, App.globalGet(EVENT_COUNT) + Int(1)),
        App.globalPut(
            Concat(EVENT_NFT_PREFIX, int_to_str(App.globalGet(EVENT_COUNT)), NFT_ID_SUFFIX),
            Btoi(Txn.application_args[1])
        ),
        App.globalPut(
            Concat(EVENT_END_PREFIX, int_to_str(App.globalGet(EVENT_COUNT))),
            Btoi(Txn.application_args[2])
        ),
        App.globalPut(
            Concat(EVENT_TICKET_COUNT_PREFIX, int_to_str(App.globalGet(EVENT_COUNT))),
            Btoi(Txn.application_args[3])
        ),
        Return(Int(1))
    ])

    stop_event = And(
        Txn.application_args.length() == Int(2),
        Txn.application_args[0] == Bytes("stop_event"),
        Txn.sender() == Global.creator_address()
    )

    handle_stop_event = Seq([
        Assert(Btoi(Txn.application_args[1]) <= App.globalGet(EVENT_COUNT)),
        Assert(Global.latest_timestamp() >= App.globalGet(
            Concat(EVENT_END_PREFIX, int_to_str(Btoi(Txn.application_args[1]))))),
        App.globalPut(
            Concat(EVENT_STOPPED_PREFIX, int_to_str(Btoi(Txn.application_args[1]))),
            Int(1)
        ),
        Return(Int(1))
    ])

    add_attendant = And(
        Txn.application_args.length() == Int(2),
        Txn.application_args[0] == Bytes("add_attendant"),
        App.globalGet(EVENT_COUNT) >= Btoi(Txn.application_args[1]),
        App.globalGet(Concat(EVENT_TICKET_COUNT_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) > Int(0)
    )

    # Cập nhật logic của handle_add_attendant mà không khai báo biến
    # Cập nhật logic của handle_add_attendant
    handle_add_attendant = Seq([
        Assert(App.globalGet(Concat(EVENT_TICKET_COUNT_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) > Int(0)),
        Assert(Not(App.localGet(Txn.sender(), Concat(EVENT_ATTENDANTS_PREFIX, int_to_str(Btoi(Txn.application_args[1])))))),
        Assert(App.globalGet(Concat(EVENT_TICKET_ISSUED_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) + Int(1) <= Int(100)),

        App.localPut(
            Txn.sender(), 
            Concat(TICKET_CODE_PREFIX, int_to_str(Btoi(Txn.application_args[1]))), 
            App.globalGet(Concat(EVENT_TICKET_ISSUED_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) + Int(1)
        ),

        App.globalPut(
            Concat(EVENT_TICKET_COUNT_PREFIX, int_to_str(Btoi(Txn.application_args[1]))), 
            App.globalGet(Concat(EVENT_TICKET_COUNT_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) - Int(1)
        ),
        
        App.globalPut(
            Concat(EVENT_TICKET_ISSUED_PREFIX, int_to_str(Btoi(Txn.application_args[1]))), 
            App.globalGet(Concat(EVENT_TICKET_ISSUED_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) + Int(1)
        ),

        Return(Int(1))
    ])


    check_in = And(
        Txn.application_args.length() == Int(3),
        Txn.application_args[0] == Bytes("check_in"),
        App.localGet(Txn.sender(), Concat(TICKET_CODE_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) == Btoi(Txn.application_args[2])  # Chuyển thành Btoi để so sánh số
    )

    handle_check_in = Seq([
        Assert(App.localGet(Txn.sender(), Concat(TICKET_CODE_PREFIX, int_to_str(Btoi(Txn.application_args[1])))) == Btoi(Txn.application_args[2])),  # Chuyển đổi mã vé từ bytes sang uint64
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [create_event, handle_create_event],
        [stop_event, handle_stop_event],
        [add_attendant, handle_add_attendant],
        [check_in, handle_check_in],
        [Txn.on_completion() == OnComplete.NoOp, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.ClearState, Return(Int(1))],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))]
    )

    return program

def clear_state_program():
    return Return(Int(1))

def generate_app_spec():
    app_spec = {
        "schema_version": 1,
        "name": "NFTicket",
        "description": "Smart contract for managing events, attendants, ticket issuance, and check-in with NFT integration.",
        "app_id": 0,  
        "creator": "Your Creator Address Here",  # Thay bằng địa chỉ thực tế của người tạo hợp đồng
        "approval_program": "approval.teal",
        "clear_state_program": "clear_state.teal",
        "global_state": {
            "schema": {
                "num_uints": 16,  # Tổng số uints được sử dụng trong global state
                "num_byte_slices": 16  # Tổng số byte slices được sử dụng trong global state
            },
            "defaults": [
                {
                    "name": "event_count",
                    "type": "uint64",
                    "description": "Total number of events created",
                    "default_value": 0
                },
                {
                    "name": "event_x_nft_id",
                    "type": "uint64",
                    "description": "NFT ID for event x",
                    "default_value": 0
                },
                {
                    "name": "event_x_end",
                    "type": "uint64",
                    "description": "End timestamp for event x",
                    "default_value": 0
                },
                {
                    "name": "event_x_stopped",
                    "type": "uint64",
                    "description": "Stopped state for event x (1 if stopped, 0 if active)",
                    "default_value": 0
                },
                {
                    "name": "event_x_ticket_count",
                    "type": "uint64",
                    "description": "Number of tickets remaining for event x",
                    "default_value": 0
                },
                {
                    "name": "event_x_ticket_issued",
                    "type": "uint64",
                    "description": "Number of tickets issued for event x",
                    "default_value": 0
                },
                {
                    "name": "event_x_current_ticket_code",
                    "type": "uint64",
                    "description": "Current ticket code for event x (incrementing from 001 to 100)",
                    "default_value": 0
                },
                {
                    "name": "event_x_attendant_slot",
                    "type": "uint64",
                    "description": "Slot assigned to each attendant for event x",
                    "default_value": 0
                },
                {
                    "name": "sender_address_x",
                    "type": "bytes",
                    "description": "Address of the sender who created event x",
                    "default_value": ""
                }
            ]
        },
        "local_state": {
            "schema": {
                "num_uints": 4,  # Mỗi người tham gia có thể lưu trạng thái của việc tham gia vào local state
                "num_byte_slices": 4  # Mã vé (ticket code) sẽ được lưu trữ dưới dạng byte
            }
        },
        "methods": [
            {
                "name": "create_event",
                "args": [
                    {
                        "type": "uint64",
                        "name": "nft_id",
                        "description": "NFT ID associated with the event"
                    },
                    {
                        "type": "uint64",
                        "name": "end_timestamp",
                        "description": "End timestamp for the event"
                    },
                    {
                        "type": "uint64",
                        "name": "ticket_count",
                        "description": "Number of tickets available for the event"
                    }
                ],
                "returns": {
                    "type": "uint64",
                    "description": "Returns 1 on success, 0 on failure"
                },
                "description": "Creates a new event with associated NFT ID, end timestamp, and available tickets."
            },
            {
                "name": "stop_event",
                "args": [
                    {
                        "type": "uint64",
                        "name": "event_id",
                        "description": "ID of the event to stop"
                    }
                ],
                "returns": {
                    "type": "uint64",
                    "description": "Returns 1 on success, 0 on failure"
                },
                "description": "Stops an event after its end timestamp has passed."
            },
            {
                "name": "add_attendant",
                "args": [
                    {
                        "type": "uint64",
                        "name": "event_id",
                        "description": "ID of the event to join"
                    }
                ],
                "returns": {
                    "type": "uint64",
                    "description": "Returns 1 on success, 0 on failure"
                },
                "description": "Registers an attendant to the specified event, issues a ticket if available."
            },
            {
                "name": "check_in",
                "args": [
                    {
                        "type": "uint64",
                        "name": "event_id",
                        "description": "ID of the event to check-in"
                    },
                    {
                        "type": "uint64",
                        "name": "ticket_code",
                        "description": "Ticket code of the attendant checking in"
                    }
                ],
                "returns": {
                    "type": "uint64",
                    "description": "Returns 1 on success, 0 on failure"
                },
                "description": "Allows an attendant to check in to the event using their ticket code."
            }
        ]
    }

    with open("application.json", "w") as json_file:
        json.dump(app_spec, json_file, indent=4)

if __name__ == "__main__":
    from pyteal import compileTeal, Mode

    with open("approval.teal", "w") as f:
        compiled_approval = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled_approval)

    with open("clear_state.teal", "w") as f:
        compiled_clear_state = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled_clear_state)

    generate_app_spec()