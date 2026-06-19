import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { Container, ContainerPayload } from '../container.model';
import { ContainersService } from '../containers.service';
import { CreateUpdateContainersComponent } from '../createUpdateContainersComponent/create-update-containers.component';
import { ViewDetailContainersComponent } from '../viewDetailContainersComponent/view-detail-containers.component';

@Component({
  selector: 'app-containers-management',
  standalone: true,
  imports: [CreateUpdateContainersComponent, ViewDetailContainersComponent],
  templateUrl: './containers-management.component.html',
  styleUrls: ['./containers-management.component.scss'],
})
export class ContainersManagementComponent implements OnInit {
  private readonly containersService = inject(ContainersService);

  currentPage = 1;
  readonly pageSize = 10;

  containers: Container[] = [];
  editingContainer: Container | null = null;
  viewingContainer: Container | null = null;
  deletingContainer: Container | null = null;
  isFormOpen = false;
  isLoading = false;
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  ngOnInit(): void {
    this.loadContainers();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.containers.length / this.pageSize));
  }

  get pagedContainers(): Container[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.containers.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  getStatusLabel(status: number): string {
    const labels: Record<number, string> = {
      0: 'Đang hoạt động',
      1: 'Đang sử dụng',
      2: 'Bảo trì',
      3: 'Ngừng dùng',
    };
    return labels[Number(status)] ?? 'Không xác định';
  }

  getTemperatureRange(container: Container): string {
    if (!container.is_temperature_controlled) {
      return 'Không kiểm soát';
    }

    const min = container.min_temperature ?? '-';
    const max = container.max_temperature ?? '-';
    return `${min}°C - ${max}°C`;
  }

  loadContainers(): void {
    this.isLoading = true;
    this.containersService.getContainers().subscribe({
      next: (containers) => {
        this.containers = containers;
        this.isLoading = false;
        this.currentPage = Math.min(this.currentPage, this.totalPages);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  openCreateForm(): void {
    this.editingContainer = null;
    this.isFormOpen = true;
  }

  openEditForm(container: Container): void {
    this.editingContainer = container;
    this.isFormOpen = true;
  }

  openDetail(container: Container): void {
    this.viewingContainer = container;
  }

  openDeleteConfirm(container: Container): void {
    this.deletingContainer = container;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingContainer = null;
  }

  saveContainer(value: ContainerPayload): void {
    const isEdit = Boolean(this.editingContainer);
    const request$ = this.editingContainer
      ? this.containersService.updateContainer(this.editingContainer.id, value)
      : this.containersService.createContainer(value);

    request$.subscribe({
      next: () => {
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật container thành công.' : 'Tạo mới container thành công.');
        this.loadContainers();
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (!this.deletingContainer) {
      return;
    }

    const containerCode = this.deletingContainer.code;
    this.containersService.deleteContainer(this.deletingContainer.id).subscribe({
      next: () => {
        this.deletingContainer = null;
        this.showToast(`Đã xóa container "${containerCode}".`);
        this.loadContainers();
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  goToPage(page: number): void {
    this.currentPage = Math.min(Math.max(page, 1), this.totalPages);
  }

  private showToast(message: string, type: 'success' | 'error' = 'success'): void {
    this.toastMessage = message;
    this.toastType = type;
    window.setTimeout(() => {
      this.toastMessage = '';
    }, 3000);
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    return typeof detail === 'string'
      ? detail
      : 'Không thể xử lý dữ liệu container. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
