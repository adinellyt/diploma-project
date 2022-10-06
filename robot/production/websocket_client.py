import json

import websocket
import rel

from main_robot import go

current_x = None
current_y = None
current_direction = "up"


def on_message(ws, message):
    global current_x, current_y, current_direction

    message_json = json.loads(message)['message']
    order_id = message_json['order_id']
    source_point_x = message_json['source_point_x']
    source_point_y = message_json['source_point_y']
    destination_point_x = message_json['destination_point_x']
    destination_point_y = message_json['destination_point_y']
    point_type = message_json['point_type']

    print(order_id, point_type, source_point_x, source_point_y, destination_point_x, destination_point_y)

    # ROBOT CODE
    is_finished = False

    if current_x is None or current_y is None:
        current_x = source_point_x
        current_y = source_point_y

    if point_type == 'source':
        print(f"Point type: {point_type}")
        print(f"From: {current_x}, {current_y}")
        print(f"To: {source_point_x}, {source_point_y}")
        print(f"Direction: {current_direction}")
        is_finished, current_direction, current_x, current_y = go(current_x, current_y, source_point_x, source_point_y, current_direction)
    elif point_type == 'destination':
        print(f"Point type: {point_type}")
        print(f"From: {current_x}, {current_y}")
        print(f"To: {destination_point_x}, {destination_point_y}")
        print(f"Direction: {current_direction}")
        is_finished, current_direction, current_x, current_y = go(current_x, current_y, destination_point_x, destination_point_y, current_direction)
    # ROBOT CODE

    response = {
        "order_id": order_id,
        "point_type": point_type,
        "is_finished": is_finished
    }
    response_text = json.dumps(response)
    ws.send(response_text)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("Closed connection to server!")


def on_open(ws):
    print("Connected to server successfully!")
    print("Waiting for orders ...")


robot_title = "aksioma"

if __name__ == "__main__":
    websocket.enableTrace(True)
    wsocket = websocket.WebSocketApp(f"wss://backend.sulaksi.kz/ws/order-delivery/{robot_title}/",
                                     on_open=on_open,
                                     on_message=on_message,
                                     on_error=on_error,
                                     on_close=on_close)

    wsocket.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
