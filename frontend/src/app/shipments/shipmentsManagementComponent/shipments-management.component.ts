import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { Batch } from '../../batches/batch.model';
import { BatchesService } from '../../batches/batches.service';
import { Container } from '../../containers/container.model';
import { ContainersService } from '../../containers/containers.service';
import { User } from '../../users/user.model';
import { UsersService } from '../../users/users.service';
import { CreateUpdateShipmentsComponent } from '../createUpdateShipmentsComponent/create-update-shipments.component';
import { Shipment, ShipmentPayload } from '../shipment.model';
import { ShipmentsService } from '../shipments.service';
import { ViewDetailShipmentsComponent } from '../viewDetailShipmentsComponent/view-detail-shipments.component';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-shipments-management',
  standalone: true,
  imports: [DatePipe, CreateUpdateShipmentsComponent, ViewDetailShipmentsComponent],
  templateUrl: './shipments-management.component.html',
  styleUrls: ['./shipments-management.component.scss'],
})
export class ShipmentsManagementComponent implements OnInit {
  private readonly shipmentsService = inject(ShipmentsService);
  private readonly batchesService = inject(BatchesService);
  private readonly usersService = inject(UsersService);
  private readonly containersService = inject(ContainersService);
  private readonly authService = inject(AuthService);

  currentPage = 1;
  readonly pageSize = 5;

  shipments: Shipment[] = [];
  batches: Batch[] = [];
  users: User[] = [];
  containers: Container[] = [];
  batchesError = '';
  usersError = '';
  containersError = '';
  isLoading = false;
  isLoadingBatches = false;
  isLoadingUsers = false;
  isLoadingContainers = false;
  editingShipment: Shipment | null = null;
  viewingShipment: Shipment | null = null;
  deletingShipment: Shipment | null = null;
  isFormOpen = false;
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  get isReadOnly(): boolean {
    return this.authService.getRole() === 3;
  }

  get isDistributor(): boolean {
    return this.authService.getRole() === 3;
  }

  readonly statusLabels: Record<number, string> = {
    0: 'Đã tạo',
    1: 'Đang vận chuyển',
    2: 'Đã giao',
    3: 'Đã hủy',
  };

  ngOnInit(): void {
    this.loadShipments();
    this.loadUsers();
    this.loadBatches();
    this.loadContainers();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.shipments.length / this.pageSize));
  }

  get pagedShipments(): Shipment[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.shipments.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  getActorName(actorId: string): string {
    return this.users.find((user) => user.id === actorId)?.full_name ?? actorId;
  }

  getStatusLabel(status: number | string): string {
    const value = Number(status);
    return this.statusLabels[value] ?? String(status);
  }

  getShipmentTitle(shipment: Shipment): string {
    return `${shipment.origin} → ${shipment.destination}`;
  }

  loadShipments(): void {
    this.isLoading = true;
    this.shipmentsService.getShipments().subscribe({
      next: (shipments) => {
        this.shipments = this.filterShipmentsByCurrentRole(shipments);
        this.isLoading = false;
        this.currentPage = Math.min(this.currentPage, this.totalPages);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  loadBatches(): void {
    this.isLoadingBatches = true;
    this.batchesError = '';
    this.batchesService.getBatches().subscribe({
      next: (batches) => {
        this.batches = batches;
        this.isLoadingBatches = false;
      },
      error: () => {
        this.batches = [];
        this.isLoadingBatches = false;
        this.batchesError = 'Không thể tải danh sách lô sản phẩm.';
      },
    });
  }

  loadUsers(): void {
    this.isLoadingUsers = true;
    this.usersError = '';
    this.usersService.getUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.isLoadingUsers = false;
      },
      error: () => {
        this.users = [];
        this.usersError = 'Không thể tải danh sách người dùng.';
        this.isLoadingUsers = false;
      },
    });
  }

  loadContainers(): void {
    this.isLoadingContainers = true;
    this.containersError = '';
    this.containersService.getContainers().subscribe({
      next: (containers) => {
        this.containers = containers;
        this.isLoadingContainers = false;
      },
      error: () => {
        this.containers = [];
        this.containersError = 'Không thể tải danh sách container.';
        this.isLoadingContainers = false;
      },
    });
  }

  openCreateForm(): void {
    if (this.isReadOnly) {
      return;
    }
    this.editingShipment = null;
    this.isFormOpen = true;
  }

  openEditForm(shipment: Shipment): void {
    if (this.isReadOnly) {
      return;
    }
    this.editingShipment = shipment;
    this.isFormOpen = true;
  }

  openDetail(shipment: Shipment): void {
    if (!this.canViewShipment(shipment)) {
      this.showToast('Bạn không có quyền xem shipment này.', 'error');
      return;
    }

    this.shipmentsService.getShipment(shipment.id).subscribe({
      next: (detail) => {
        if (!this.canViewShipment(detail)) {
          this.showToast('Bạn không có quyền xem shipment này.', 'error');
          return;
        }

        this.viewingShipment = detail;
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  openDeleteConfirm(shipment: Shipment): void {
    if (this.isReadOnly) {
      return;
    }
    this.deletingShipment = shipment;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingShipment = null;
  }

  saveShipment(value: ShipmentPayload): void {
    if (this.isReadOnly) {
      return;
    }
    const isEdit = Boolean(this.editingShipment);
    const request$ = this.editingShipment
      ? this.shipmentsService.updateShipment(this.editingShipment.id, value)
      : this.shipmentsService.createShipment(value);

    request$.subscribe({
      next: () => {
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật shipment thành công.' : 'Tạo mới shipment thành công.');
        this.loadShipments();
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (this.isReadOnly || !this.deletingShipment) {
      return;
    }

    const shipmentTitle = this.getShipmentTitle(this.deletingShipment);
    this.shipmentsService.deleteShipment(this.deletingShipment.id).subscribe({
      next: () => {
        this.deletingShipment = null;
        this.showToast(`Đã xóa shipment "${shipmentTitle}".`);
        this.loadShipments();
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

  private filterShipmentsByCurrentRole(shipments: Shipment[]): Shipment[] {
    const currentUser = this.authService.getCurrentUser();

    if (!this.isDistributor || !currentUser) {
      return shipments;
    }

    return shipments.filter((shipment) => shipment.to_actor_id === currentUser.id);
  }

  private canViewShipment(shipment: Shipment): boolean {
    const currentUser = this.authService.getCurrentUser();

    if (!this.isDistributor || !currentUser) {
      return true;
    }

    return shipment.to_actor_id === currentUser.id;
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    if (typeof detail === 'string') {
      return detail;
    }
    if (error.status === 404 || error.status === 405) {
      return 'API backend hiện chưa hỗ trợ thao tác này cho shipment.';
    }
    return 'Không thể xử lý dữ liệu shipment. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
