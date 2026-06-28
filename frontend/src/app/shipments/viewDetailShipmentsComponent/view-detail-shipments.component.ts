import { DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Batch } from '../../batches/batch.model';
import { Container } from '../../containers/container.model';
import { User } from '../../users/user.model';
import { Shipment } from '../shipment.model';

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

  getBatchLabel(batchId: string): string {
    return batchId;
  }

  getContainerLabel(containerId: string): string {
    const container = this.containers.find((currentContainer) => currentContainer.id === containerId);
    return container ? `${container.code} - ${container.type}` : containerId;
  }

  getContainerCapacity(containerId: string): string {
    const container = this.containers.find((currentContainer) => currentContainer.id === containerId);
    return container ? `${container.capacity} ${container.capacity_unit}` : 'Chưa cập nhật';
  }
}
