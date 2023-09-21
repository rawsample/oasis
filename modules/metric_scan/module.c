#include "types.h"
#include "metrics.h"
#include "callbacks.h"
#include "wrapper.h"
#include "monitor.h"
#include "messages.h"

#define PACKET_SIZE sizeof(packet_t)
#define CONN_SIZE sizeof(connection_t)
#define LDEV_SIZE sizeof(local_device_t)
#define RDEV_SIZE sizeof(remote_device_t)
#define METRIC_SIZE 2 + PACKET_SIZE + CONN_SIZE + LDEV_SIZE + RDEV_SIZE

void SCAN_CALLBACK(metric_scan)(metrics_t * metrics) {
  uint8_t idx = 0;
  uint8_t message[METRIC_SIZE];
  packet_t *pkg;
  connection_t *conn;
  local_device_t *ldev;
  remote_device_t *rdev;

  /* Header */
  message[0] = MESSAGE_TYPE_METRIC;
  message[1] = OPCODE_MONITOR_RX_SCAN;
  idx = 2;

  /* Copy current_packet */
  pkg = metrics->current_packet;
  memcpy(message + idx, &pkg, PACKET_SIZE);
  idx += PACKET_SIZE;

  /* Copy current_connection */
  conn = metrics->current_connection;
  memcpy(message + idx, &conn, CONN_SIZE);
  idx += CONN_SIZE;

  /* Copy local_device */
  ldev = metrics->local_device;
  memcpy(message + idx, &ldev, LDEV_SIZE);
  idx += LDEV_SIZE;

  /* Copy remote_device */
  rdev = metrics->remote_device;
  memcpy(message + idx, &rdev, RDEV_SIZE);
  idx += RDEV_SIZE;

  /* Send it through HCI */
  log(message, idx);
}

