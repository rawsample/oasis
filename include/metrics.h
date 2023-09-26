#ifndef METRICS_H
#define METRICS_H

#include "types.h"
#include "packet.h"
#include "device.h"
#include "connection.h"


#define OPCODE_METRIC_TIME 0x00
#define OPCODE_METRIC_RX_SCAN 0x01
#define OPCODE_METRIC_INIT_CONN 0x02
#define OPCODE_METRIC_DELETE_CONN 0x03
#define OPCODE_METRIC_RX_CONN 0x04
#define OPCODE_METRIC_TX_CONN 0x05


typedef struct metrics {
  packet_t *current_packet;
  connection_t *current_connection;
  local_device_t *local_device;
  remote_device_t *remote_device;
} metrics_t;

#endif
