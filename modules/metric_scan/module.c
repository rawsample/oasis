#include "types.h"
#include "metrics.h"
#include "callbacks.h"
#include "wrapper.h"
#include "monitor.h"
#include "messages.h"

#define PACKET_SIZE sizeof(packet_t)        // 268
#define CONN_SIZE sizeof(connection_t)
#define LDEV_SIZE sizeof(local_device_t)
#define RDEV_SIZE sizeof(remote_device_t)
#define METRIC_SIZE 2 + PACKET_SIZE + CONN_SIZE + LDEV_SIZE + RDEV_SIZE

void SCAN_CALLBACK(metric_scan)(metrics_t * metrics) {
  uint8_t idx = 0;
  uint8_t payload_size;
  uint8_t message[METRIC_SIZE];
  packet_t *pkg;
  connection_t *conn;
  local_device_t *ldev;
  remote_device_t *rdev;

  /* Header */
  message[0] = MESSAGE_TYPE_METRIC;
  message[1] = OPCODE_METRIC_RX_SCAN;
  idx = 2;

  /* Copy current_packet */
  pkg = metrics->current_packet;
  memcpy(message + idx, &pkg->timestamp, sizeof(uint32_t));
  idx += sizeof(uint32_t);
  memcpy(message + idx, &pkg->valid, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &pkg->channel, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &pkg->rssi, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &pkg->header, 2*sizeof(uint8_t));
  idx += 2*sizeof(uint8_t);

  payload_size = get_packet_size();
  memcpy(message + idx, &payload_size, sizeof(payload_size));
  idx += sizeof(payload_size);
  memcpy(message + idx, &pkg->content, payload_size*sizeof(uint8_t));
  idx += payload_size*sizeof(uint8_t);

  /* Copy current_connection */
  conn = metrics->current_connection;
  memcpy(message + idx, &conn->access_address, sizeof(uint32_t));
  idx += sizeof(uint32_t);
  memcpy(message + idx, &conn->crc_init, sizeof(uint32_t));
  idx += sizeof(uint32_t);
  memcpy(message + idx, &conn->hop_interval, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &conn->packets_lost_counter, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &conn->tx_counter, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &conn->rx_counter, sizeof(uint16_t));
  idx += sizeof(uint16_t);
  memcpy(message + idx, &conn->channel_map, 5*sizeof(uint8_t));
  idx += 5*sizeof(uint8_t);

  /* Copy local_device */
  ldev = metrics->local_device;
  memcpy(message + idx, &ldev->gap_role, sizeof(gap_role_t));
  idx += sizeof(gap_role_t);
  memcpy(message + idx, &ldev->address, 6*sizeof(uint8_t));
  idx += 6*sizeof(uint8_t);

  /* Copy remote_device */
  rdev = metrics->remote_device;
  memcpy(message + idx, &rdev->address_type, sizeof(address_type_t));
  idx += sizeof(address_type_t);
  memcpy(message + idx, &rdev->gap_role, sizeof(gap_role_t));
  idx += sizeof(gap_role_t);
  memcpy(message + idx, &rdev->address, 6*sizeof(uint8_t));
  idx += 6*sizeof(uint8_t);
  /*
   * Warning: change the python side
  #ifdef SCAN_ENABLED
  memcpy(message + idx, &rdev->advertisements_interval, sizeof(uint32_t));
  idx += sizeof(uint32_t);
  #endif
  #ifdef CONNECTION_ENABLED
  memcpy(message + idx, &rdev->connection_interval, sizeof(uint32_t));
  idx += sizeof(uint32_t);
  #endif
  */

  ///* 
  // * Check the struct values during compile-time.
  // * If these assert would failed, it would be necessary to update the python part.
  // */
  //_Static_assert(PACKET_SIZE == 268, "Wrong guess for PACKET_SIZE");
  //_Static_assert(CONN_SIZE == 24, "Wrong guess for CONN_SIZE");
  //_Static_assert(LDEV_SIZE == 7, "Wrong guess for LDEV_SIZE");
  //_Static_assert(RDEV_SIZE == 12, "Wrong guess for RDEV_SIZE");
  //_Static_assert(METRIC_SIZE == 313, "Wrong guess for METRIC_SIZE");

  /* Send it through HCI */
  log(message, idx);
}

