import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { CropType, CropTypePayload } from '../crop-type.model';
import { CropTypesService } from '../crop-types.service';
import { CreateUpdateCropTypesComponent } from '../createUpdateCropTypesComponent/create-update-crop-types.component';
import { ViewDetailCropTypesComponent } from '../viewDetailCropTypesComponent/view-detail-crop-types.component';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-crop-types-management',
  standalone: true,
  imports: [CreateUpdateCropTypesComponent, ViewDetailCropTypesComponent],
  templateUrl: './crop-types-management.component.html',
  styleUrls: ['./crop-types-management.component.scss'],
})
export class CropTypesManagementComponent implements OnInit {
  private readonly cropTypesService = inject(CropTypesService);
  private readonly authService = inject(AuthService);

  currentPage = 1;
  readonly pageSize = 10;

  cropTypes: CropType[] = [];
  editingCropType: CropType | null = null;
  viewingCropType: CropType | null = null;
  deletingCropType: CropType | null = null;
  isFormOpen = false;
  isLoading = false;
  isSaving = false;
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  get isReadOnly(): boolean {
    return this.authService.getRole() !== 0;
  }

  ngOnInit(): void {
    this.loadCropTypes();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.cropTypes.length / this.pageSize));
  }

  get pagedCropTypes(): CropType[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.cropTypes.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  loadCropTypes(): void {
    this.isLoading = true;
    this.cropTypesService.getCropTypes().subscribe({
      next: (cropTypes) => {
        this.cropTypes = cropTypes;
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
    if (this.isReadOnly) {
      return;
    }
    this.editingCropType = null;
    this.isFormOpen = true;
  }

  openEditForm(cropType: CropType): void {
    if (this.isReadOnly) {
      return;
    }
    this.editingCropType = cropType;
    this.isFormOpen = true;
  }

  openDetail(cropType: CropType): void {
    this.viewingCropType = cropType;
  }

  openDeleteConfirm(cropType: CropType): void {
    if (this.isReadOnly) {
      return;
    }
    this.deletingCropType = cropType;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingCropType = null;
  }

  saveCropType(value: CropTypePayload): void {
    if (this.isReadOnly || this.isSaving) {
      return;
    }
    this.isSaving = true;
    const isEdit = Boolean(this.editingCropType);
    const request$ = this.editingCropType
      ? this.cropTypesService.updateCropType(this.editingCropType.id, value)
      : this.cropTypesService.createCropType(value);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật loại nông sản thành công.' : 'Tạo mới loại nông sản thành công.');
        this.loadCropTypes();
      },
      error: (error: HttpErrorResponse) => {
        this.isSaving = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (this.isReadOnly || !this.deletingCropType) {
      return;
    }

    const cropTypeName = this.deletingCropType.name;
    this.cropTypesService.deleteCropType(this.deletingCropType.id).subscribe({
      next: () => {
        this.deletingCropType = null;
        this.showToast(`Đã xóa loại nông sản "${cropTypeName}".`);
        this.loadCropTypes();
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
      : 'Không thể xử lý dữ liệu loại nông sản. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
