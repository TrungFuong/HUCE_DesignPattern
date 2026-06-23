import { DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Batch } from '../../batches/batch.model';
import { Container } from '../../containers/container.model';
import { User } from '../../users/user.model';
import { Shipment, ShipmentItem } from '../shipment.model';

@Component({
  selector: 'app-view-detail-shipments',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './view-detail-shipments.component.html',
  styleUrls: ['./view-detail-shipments.component.scss'],
})
export class ViewDetailShipmentsComponent {
  @Input({ required: true }) shipment!: Shipment;
  @Input() users: User[] = [];
  @Input() batches: Batch[] = [];
  @Input() containers: Container[] = [];
  @Output() close = new EventEmitter<void>();

  readonly statusLabels: Record<number, string> = {
    0: 'Đã tạo',
    1: 'Đang vận chuyển',
    2: 'Đã giao',
    3: 'Đã hủy',
  };

  getActorName(actorId: string): string {
    return this.users.find((user) => user.id === actorId)?.full_name ?? actorId;
  }

  getStatusLabel(status: number | string): string {
    const value = Number(status);
    return this.statusLabels[value] ?? String(status);
  }

  getBatchLabel(item: ShipmentItem): string {
    return item.product_name
      ?? this.batches.find((batch) => batch.id === item.batch_id)?.product_name
      ?? item.batch_id;
  }

  getContainerLabel(item: ShipmentItem): string {
    if (item.container_code) {
      return `${item.container_code}${item.container_type ? ` - ${item.container_type}` : ''}`;
    }
    const container = this.containers.find((currentContainer) => currentContainer.id === item.container_id);
    return container ? `${container.code} - ${container.type}` : item.container_id;
  }

  getContainerCapacity(item: ShipmentItem): string {
    if (item.container_capacity !== null && item.container_capacity !== undefined) {
      return `${item.container_capacity} ${item.container_capacity_unit ?? ''}`.trim();
    }
    const container = this.containers.find((currentContainer) => currentContainer.id === item.container_id);
    return container ? `${container.capacity} ${container.capacity_unit}` : 'Chưa cập nhật';
  }
}
