import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Batch } from '../../batches/batch.model';
import { Container } from '../../containers/container.model';
import { User } from '../../users/user.model';
import { Shipment, ShipmentItem, ShipmentPayload } from '../shipment.model';

@Component({
  selector: 'app-create-update-shipments',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-shipments.component.html',
  styleUrls: ['./create-update-shipments.component.scss'],
})
export class CreateUpdateShipmentsComponent implements OnChanges {
  @Input() shipment: Shipment | null = null;
  @Input() users: User[] = [];
  @Input() usersError = '';
  @Input() isLoadingUsers = false;
  @Input() batches: Batch[] = [];
  @Input() batchesError = '';
  @Input() isLoadingBatches = false;
  @Input() containers: Container[] = [];
  @Input() containersError = '';
  @Input() isLoadingContainers = false;
  @Input() isSaving = false;

  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<ShipmentPayload>();

  readonly statusOptions = [
    { value: 0, label: 'Đã tạo' },
    { value: 1, label: 'Đang vận chuyển' },
    { value: 2, label: 'Đã giao' },
    { value: 3, label: 'Đã hủy' },
  ];

  form = this.createEmptyForm();

  get title(): string {
    return this.shipment ? 'Cập nhật shipment' : 'Tạo shipment mới';
  }

  get senderUsers(): User[] {
    return this.users.filter((user) => user.is_active && user.role === 1);
  }

  get receiverUsers(): User[] {
    return this.users.filter((user) => user.is_active && user.role === 3);
  }

  get carrierUsers(): User[] {
    return this.users.filter((user) => user.is_active && user.role === 2);
  }

  get selectableContainers(): Container[] {
    const existingContainerIds = new Set(
      this.shipment?.items.map((item) => item.container_id) ?? [],
    );
    return this.containers.filter(
      (container) =>
        Number(container.status) === 0 ||
        Number(container.status) === 1 ||
        existingContainerIds.has(container.id),
    );
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['shipment']) {
      this.form = this.shipment ? this.buildFormFromShipment(this.shipment) : this.createEmptyForm();
    }
  }

  addItem(): void {
    this.form.items = [...this.form.items, this.createEmptyItem()];
  }

  removeItem(index: number): void {
    if (this.form.items.length === 1) {
      return;
    }

    this.form.items = this.form.items.filter((_, itemIndex) => itemIndex !== index);
  }

  applyBatchUnit(item: ShipmentItem): void {
    const batch = this.batches.find((currentBatch) => currentBatch.id === item.batch_id);
    if (batch) {
      item.quantity_unit = batch.quantity_unit;
    }
  }

  getBatchLabel(batch: Batch): string {
    return batch.product_name;
  }

  getContainerLabel(container: Container): string {
    return `${container.code} - ${container.type} (${container.capacity} ${container.capacity_unit})`;
  }

  cancelForm(): void {
    this.cancel.emit();
  }

  submit(): void {
    if (this.isSaving) {
      return;
    }
    const payload: ShipmentPayload = {
      id: this.shipment?.id,
      from_actor_id: this.form.from_actor_id,
      to_actor_id: this.form.to_actor_id,
      carrier_id: this.form.carrier_id,
      origin: this.form.origin.trim(),
      destination: this.form.destination.trim(),
      status: Number(this.form.status),
      start_time: new Date(this.form.start_time).toISOString(),
      end_time: this.form.end_time ? new Date(this.form.end_time).toISOString() : null,
      notes: this.form.notes.trim() || null,
      items: this.form.items.map((item) => ({
        id: item.id,
        batch_id: item.batch_id,
        container_id: item.container_id,
        quantity: Number(item.quantity) || 1,
        quantity_unit: item.quantity_unit.trim() || 'kg',
      })),
    };

    this.save.emit(payload);
  }

  private createEmptyForm() {
    return {
      from_actor_id: '',
      to_actor_id: '',
      carrier_id: '',
      origin: '',
      destination: '',
      status: 0,
      start_time: this.toDateTimeInputValue(new Date()),
      end_time: '',
      notes: '',
      items: [this.createEmptyItem()],
    };
  }

  private createEmptyItem(): ShipmentItem {
    return {
      batch_id: '',
      container_id: '',
      quantity: 1,
      quantity_unit: 'kg',
    };
  }

  private buildFormFromShipment(shipment: Shipment) {
    return {
      from_actor_id: shipment.from_actor_id,
      to_actor_id: shipment.to_actor_id,
      carrier_id: shipment.carrier_id,
      origin: shipment.origin,
      destination: shipment.destination,
      status: Number(shipment.status),
      start_time: this.toDateTimeInputValue(shipment.start_time),
      end_time: shipment.end_time ? this.toDateTimeInputValue(shipment.end_time) : '',
      notes: shipment.notes ?? '',
      items: shipment.items.length
        ? shipment.items.map((item) => ({
            id: item.id,
            shipment_id: item.shipment_id,
            batch_id: item.batch_id,
            container_id: item.container_id,
            quantity: item.quantity,
            quantity_unit: item.quantity_unit,
          }))
        : [this.createEmptyItem()],
    };
  }

  private toDateTimeInputValue(value: Date | string | null): string {
    const date = value ? new Date(value) : new Date();
    const pad = (num: number) => String(num).padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
  }
}
