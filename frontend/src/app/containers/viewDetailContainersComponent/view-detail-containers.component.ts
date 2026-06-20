import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Container } from '../container.model';

@Component({
  selector: 'app-view-detail-containers',
  standalone: true,
  templateUrl: './view-detail-containers.component.html',
  styleUrls: ['./view-detail-containers.component.scss'],
})
export class ViewDetailContainersComponent {
  @Input({ required: true }) container!: Container;
  @Output() close = new EventEmitter<void>();

  getStatusLabel(status: number): string {
    const labels: Record<number, string> = {
      0: 'Đang hoạt động',
      1: 'Đang sử dụng',
      2: 'Bảo trì',
      3: 'Ngừng dùng',
    };
    return labels[Number(status)] ?? 'Không xác định';
  }

  getTemperatureRange(): string {
    if (!this.container.is_temperature_controlled) {
      return 'Không kiểm soát';
    }

    const min = this.container.min_temperature ?? '-';
    const max = this.container.max_temperature ?? '-';
    return `${min}°C - ${max}°C`;
  }
}
