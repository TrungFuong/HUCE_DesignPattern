import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { CropType } from '../../crop-types/crop-type.model';
import { CropTypesService } from '../../crop-types/crop-types.service';
import { Farm } from '../../farms/farm.model';
import { FarmsService } from '../../farms/farms.service';
import { Batch, BatchPayload } from '../batch.model';
import { BatchesService } from '../batches.service';
import { CreateUpdateBatchesComponent } from '../createUpdateBatchesComponent/create-update-batches.component';
import { ShowQrBatchesComponent } from '../showQrBatchesComponent/show-qr-batches.component';
import { ViewDetailBatchesComponent } from '../viewDetailBatchesComponent/view-detail-batches.component';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-batches-management',
  standalone: true,
  imports: [DatePipe, CreateUpdateBatchesComponent, ViewDetailBatchesComponent, ShowQrBatchesComponent],
  templateUrl: './batches-management.component.html',
  styleUrls: ['./batches-management.component.scss'],
})
export class BatchesManagementComponent implements OnInit {
  private readonly batchesService = inject(BatchesService);
  private readonly farmsService = inject(FarmsService);
  private readonly cropTypesService = inject(CropTypesService);
  private readonly authService = inject(AuthService);

  currentPage = 1;
  readonly pageSize = 5;

  batches: Batch[] = [];
  farms: Farm[] = [];
  cropTypes: CropType[] = [];
  farmsError = '';
  cropTypesError = '';
  isLoadingFarms = false;
  isLoadingCropTypes = false;
  editingBatch: Batch | null = null;
  viewingBatch: Batch | null = null;
  deletingBatch: Batch | null = null;
  qrBatch: Batch | null = null;
  isFormOpen = false;
  isLoading = false;
  isSaving = false;
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  get isReadOnly(): boolean {
    return this.authService.getRole() === 2;
  }

  ngOnInit(): void {
    this.loadBatches();
    this.loadFarms();
    this.loadCropTypes();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.batches.length / this.pageSize));
  }

  get pagedBatches(): Batch[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.batches.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  getFarmName(farmId: string): string {
    return this.farms.find((farm) => farm.id === farmId)?.name ?? farmId;
  }

  getCropTypeName(cropTypeId: string | null): string {
    if (!cropTypeId) {
      return 'Không có';
    }
    return this.cropTypes.find((cropType) => cropType.id === cropTypeId)?.name ?? cropTypeId;
  }

  getQrImageUrl(batch: Batch): string {
    return this.batchesService.getQrImageUrl(batch.id);
  }

  getPublicTraceUrl(batch: Batch): string {
    return this.batchesService.getPublicTraceUrl(batch.id);
  }

  loadBatches(): void {
    this.isLoading = true;
    this.batchesService.getBatches().subscribe({
      next: (batches) => {
        this.batches = batches;
        this.isLoading = false;
        this.currentPage = Math.min(this.currentPage, this.totalPages);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  loadFarms(): void {
    this.isLoadingFarms = true;
    this.farmsError = '';
    this.farmsService.getFarms().subscribe({
      next: (farms) => {
        this.farms = farms;
        this.isLoadingFarms = false;
      },
      error: () => {
        this.farms = [];
        this.farmsError = 'Không thể tải danh sách nông trại.';
        this.isLoadingFarms = false;
      },
    });
  }

  loadCropTypes(): void {
    this.isLoadingCropTypes = true;
    this.cropTypesError = '';
    this.cropTypesService.getCropTypes().subscribe({
      next: (cropTypes) => {
        this.cropTypes = cropTypes;
        this.isLoadingCropTypes = false;
      },
      error: () => {
        this.cropTypes = [];
        this.cropTypesError = 'Không thể tải danh sách loại nông sản.';
        this.isLoadingCropTypes = false;
      },
    });
  }

  openCreateForm(): void {
    this.editingBatch = null;
    this.isFormOpen = true;
  }

  openEditForm(batch: Batch): void {
    this.editingBatch = batch;
    this.isFormOpen = true;
  }

  openDetail(batch: Batch): void {
    this.viewingBatch = batch;
  }

  openQr(batch: Batch): void {
    this.qrBatch = batch;
  }

  openDeleteConfirm(batch: Batch): void {
    this.deletingBatch = batch;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingBatch = null;
  }

  saveBatch(value: BatchPayload): void {
    if (this.isSaving) {
      return;
    }
    this.isSaving = true;
    const isEdit = Boolean(this.editingBatch);
    const request$ = this.editingBatch
      ? this.batchesService.updateBatch(this.editingBatch.id, value)
      : this.batchesService.createBatch(value);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật lô sản phẩm thành công. QR đã được tạo mới.' : 'Tạo mới lô sản phẩm thành công. QR đã được tạo.');
        this.loadBatches();
      },
      error: (error: HttpErrorResponse) => {
        this.isSaving = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (!this.deletingBatch) {
      return;
    }

    const productName = this.deletingBatch.product_name;
    this.batchesService.deleteBatch(this.deletingBatch.id).subscribe({
      next: () => {
        this.deletingBatch = null;
        this.showToast(`Đã xóa lô sản phẩm "${productName}".`);
        this.loadBatches();
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
      : 'Không thể xử lý dữ liệu lô sản phẩm. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
