import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { CreateUpdateFarmsComponent } from '../createUpdateFarmsComponent/create-update-farms.component';
import { Farm, FarmPayload } from '../farm.model';
import { FarmsService } from '../farms.service';
import { ViewDetailFarmsComponent } from '../viewDetailFarmsComponent/view-detail-farms.component';
import { User } from '../../users/user.model';
import { UsersService } from '../../users/users.service';

@Component({
  selector: 'app-farms-management',
  standalone: true,
  imports: [DatePipe, CreateUpdateFarmsComponent, ViewDetailFarmsComponent],
  templateUrl: './farms-management.component.html',
  styleUrls: ['./farms-management.component.scss'],
})
export class FarmsManagementComponent implements OnInit {
  private readonly farmsService = inject(FarmsService);
  private readonly usersService = inject(UsersService);

  currentPage = 1;
  readonly pageSize = 10;

  farms: Farm[] = [];
  farmers: User[] = [];
  editingFarm: Farm | null = null;
  viewingFarm: Farm | null = null;
  deletingFarm: Farm | null = null;
  isFormOpen = false;
  isLoading = false;
  isSaving = false;
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  ngOnInit(): void {
    this.loadFarms();
    this.loadFarmers();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.farms.length / this.pageSize));
  }

  get pagedFarms(): Farm[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.farms.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  getOwnerName(ownerId: string): string {
    return this.farmers.find((farmer) => farmer.id === ownerId)?.full_name ?? ownerId;
  }

  loadFarms(): void {
    this.isLoading = true;
    this.farmsService.getFarms().subscribe({
      next: (farms) => {
        this.farms = farms;
        this.isLoading = false;
        this.currentPage = Math.min(this.currentPage, this.totalPages);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  loadFarmers(): void {
    this.usersService.getFarmers().subscribe({
      next: (farmers) => {
        this.farmers = farmers;
      },
      error: () => {
        this.farmers = [];
      },
    });
  }

  openCreateForm(): void {
    this.editingFarm = null;
    this.isFormOpen = true;
  }

  openEditForm(farm: Farm): void {
    this.editingFarm = farm;
    this.isFormOpen = true;
  }

  openDetail(farm: Farm): void {
    this.viewingFarm = farm;
  }

  openDeleteConfirm(farm: Farm): void {
    this.deletingFarm = farm;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingFarm = null;
  }

  saveFarm(value: FarmPayload): void {
    this.isSaving = true;
    const isEdit = Boolean(this.editingFarm);
    const request$ = this.editingFarm
      ? this.farmsService.updateFarm(this.editingFarm.id, value)
      : this.farmsService.createFarm(value);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật nông trại thành công.' : 'Tạo mới nông trại thành công.');
        this.loadFarms();
      },
      error: (error: HttpErrorResponse) => {
        this.isSaving = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (!this.deletingFarm) {
      return;
    }

    const farmName = this.deletingFarm.name;
    this.farmsService.deleteFarm(this.deletingFarm.id).subscribe({
      next: () => {
        this.deletingFarm = null;
        this.showToast(`Đã xóa nông trại "${farmName}".`);
        this.loadFarms();
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
      : 'Không thể xử lý dữ liệu nông trại. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
