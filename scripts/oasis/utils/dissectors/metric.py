import struct
import json

from enum import IntEnum


class OPCODE_MONITOR(IntEnum):
    TIME = 0
    RX_SCAN = 1
    INIT_CONN = 2
    RX_CONN = 3

class ADDRESS_TYPE(IntEnum):
    PUBLIC = 0
    RANDOM = 1

class ADV_TYPE(IntEnum):
    ADV_IND = 0
    ADV_DIRECT_IND = 1
    ADV_NONCONN_IND = 2
    SCAN_REQ = 3
    SCAN_RSP = 4
    CONNECT_REQ = 5
    ADV_SCAN_IND = 6

class GAP_ROLE(IntEnum):
    ADVERTISER = 0
    PERIPHERAL = 1
    SCANNER = 2
    CENTRAL = 3              


SIZE_CONN = 21
SIZE_LDEV = 7
SIZE_RDEV = 8

# String format used to unpack the data
format_packet = "<IHHH2BB"
format_conn = "<IIBHHH5B"
format_ldev = "<B6B"
format_rdev = "<BB6B"   # NOTE: advertisements_interval and connection_interval are not included



def parse_metric_message(message):
    assert message[0] == OPCODE_MONITOR.RX_SCAN, f"Error: wrong opcode: {message[0]}"

    message = message[1:]
    print(len(message))
    print(message)

    # Unpack packet_t
    packet_offset = 0
    content_offset = packet_offset + 13

    raw_packet = message[packet_offset:content_offset]
    data_packet = struct.unpack(format_packet, raw_packet)

    content_size = message[content_offset]
    content_size_bis = data_packet[6]
    assert content_size == content_size_bis, f"Error payload_size {content_size_bis} != {content_size}"
    content_end_offset = content_offset + content_size_bis
    raw_content = message[content_offset:content_end_offset]
    packet = {
        'timestamp': data_packet[0],
        'valid': data_packet[1],
        'channel': data_packet[2],
        'rssi': data_packet[3],
        'header': data_packet[4:6],
        'content': raw_content,
    }

    print(packet)

    # Set struct offsets
    conn_offset = content_end_offset
    ldev_offset = conn_offset + 20
    rdev_offset = ldev_offset + 7
    rdev_end = rdev_offset + 8

    # Unpack connenction_t
    raw_conn = message[conn_offset:ldev_offset]
    print(raw_conn)
    data_conn = struct.unpack(format_conn, raw_conn)
    conn = {
        'access_address': data_conn[0],
        'crc_init': data_conn[1],
        'hop_interval': data_conn[2],
        'packets_lost_counter': data_conn[3],
        'tx_counter': data_conn[4],
        'rx_counter': data_conn[5],
        'channel_map': data_conn[6:11],
    }

    print(conn)

    # Unpack local_device_t
    raw_ldev = message[ldev_offset:rdev_offset]
    print(raw_ldev)
    data_ldev = struct.unpack(format_ldev, raw_ldev)
    ldev = {
        'gap_role': data_ldev[0],
        'address': data_ldev[1:7],
    }

    print(ldev)

    # Unpack remote_device_t
    # NOTE: advertisements_interval and connection_interval are not included
    raw_rdev = message[rdev_offset:rdev_end]
    print(raw_rdev)
    data_rdev = struct.unpack(format_rdev, raw_rdev)
    rdev = {
        'address_type': data_ldev[0],
        'gap_role': data_ldev[1],
        'address': data_ldev[2:8],
        #advertisements_interval
        #connection_interval
    }

    print(rdev)

    # The metrics as passed to the module through callbacks
    metrics = {
        'current_packet': packet,
        'current_connection': conn,
        'local_device': ldev,
        'remote_device': rdev,
    }
    return metrics


def format_metric_message(message):
    return message



