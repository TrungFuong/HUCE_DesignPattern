import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Container, ContainerPayload } from '../container.model';

@Component({
  selector: 'app-create-update-containers',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-containers.component.html',
  styleUrls: ['./create-update-containers.component.scss'],
})
export class CreateUpdateContainersComponent implements OnChanges {
  @Input() container: Container | null = null;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<ContainerPayload>();

  readonly statusOptions = [
    { value: 0, label: 'Đang hoạt động' },
    { value: 1, label: 'Đang sử dụng' },
    { value: 2, label: 'Bảo trì' },
    { value: 3, label: 'Ngừng dùng' },
  ];

  form = this.createEmptyForm();

  get title(): string {
    return this.container ? 'Cập nhật container' : 'Tạo container mới';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['container']) {
      this.form = this.container
        ? {
            code: this.container.code,
            type: this.container.type,
            capacity: this.container.capacity,
            capacity_unit: this.container.capacity_unit,
            material: this.container.material ?? '',
            is_temperature_controlled: this.container.is_temperature_controlled,
            min_temperature: this.container.min_temperature,
            max_temperature: this.container.max_temperature,
            status: Number(this.container.status),
            description: this.container.description ?? '',
          }
        : this.createEmptyForm();
    }
  }

  toggleTemperatureControl(): void {
    if (!this.form.is_temperature_controlled) {
      this.form.min_temperature = null;
      this.form.max_temperature = null;
    }
  }

  submit(): void {
    const isTemperatureControlled = Boolean(this.form.is_temperature_controlled);
    const payload: ContainerPayload = {
      id: this.container?.id,
      code: this.form.code.trim().toUpperCase(),
      type: this.form.type.trim(),
      capacity: Number(this.form.capacity),
      capacity_unit: this.form.capacity_unit.trim() || 'kg',
      material: this.form.material.trim() || null,
      is_temperature_controlled: isTemperatureControlled,
      min_temperature: isTemperatureControlled ? this.toNullableNumber(this.form.min_temperature) : null,
      max_temperature: isTemperatureControlled ? this.toNullableNumber(this.form.max_temperature) : null,
      status: Number(this.form.status),
      description: this.form.description.trim() || null,
    };

    this.save.emit(payload);
  }

  private createEmptyForm() {
    return {
      code: '',
      type: '',
      capacity: 1,
      capacity_unit: 'kg',
      material: '',
      is_temperature_controlled: false,
      min_temperature: null as number | null,
      max_temperature: null as number | null,
      status: 0,
      description: '',
    };
  }

  private toNullableNumber(value: number | string | null): number | null {
    if (value === null || value === '') {
      return null;
    }
    return Number(value);
  }
}
