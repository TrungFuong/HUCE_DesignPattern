import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { forkJoin } from 'rxjs';
import { AuthService } from '../../auth.service';
import { Chemical } from '../../chemicals/chemical.model';
import { ChemicalsService } from '../../chemicals/chemicals.service';
import { CropType } from '../../crop-types/crop-type.model';
import { CropTypesService } from '../../crop-types/crop-types.service';
import { Farm } from '../../farms/farm.model';
import { FarmsService } from '../../farms/farms.service';
import { BatchChemicalsComponent } from '../batchChemicalsComponent/batch-chemicals.component';
import { Batch, BatchChemicalItem, BatchPayload } from '../batch.model';
import { BatchesService } from '../batches.service';
import { CreateUpdateBatchesComponent } from '../createUpdateBatchesComponent/create-update-batches.component';
import { ShowQrBatchesComponent } from '../showQrBatchesComponent/show-qr-batches.component';
import { ViewDetailBatchesComponent } from '../viewDetailBatchesComponent/view-detail-batches.component';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-batches-management',
  standalone: true,
  imports: [
    DatePipe,
    CreateUpdateBatchesComponent,
    ViewDetailBatchesComponent,
    ShowQrBatchesComponent,
    BatchChemicalsComponent,
  ],
  templateUrl: './batches-management.component.html',
  styleUrls: ['./batches-management.component.scss'],
})
export class BatchesManagementComponent implements OnInit {
  private readonly batchesService = inject(BatchesService);
  private readonly farmsService = inject(FarmsService);
  private readonly cropTypesService = inject(CropTypesService);
  private readonly authService = inject(AuthService);
<<<<<<< HEAD
=======
  private readonly chemicalsService = inject(ChemicalsService);
>>>>>>> d89c627d97b7aff05863d4f6aa41fd754b888870

  currentPage = 1;
  readonly pageSize = 5;

  batches: Batch[] = [];
  private allBatches: Batch[] = [];
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
  chemicalBatch: Batch | null = null;
  isFormOpen = false;
  isLoading = false;
<<<<<<< HEAD
  isSaving = false;
=======
  isLoadingChemicals = false;
  chemicals: Chemical[] = [];
  batchChemicals: BatchChemicalItem[] = [];
  chemicalsError = '';
>>>>>>> d89c627d97b7aff05863d4f6aa41fd754b888870
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  get isReadOnly(): boolean {
<<<<<<< HEAD
    return this.authService.getRole() === 2;
=======
    return !this.canWriteBatch;
  }

  get canWriteBatch(): boolean {
    const role = this.authService.getRole();
    return role === 0 || role === 1;
  }

  get isFarmer(): boolean {
    return this.authService.getRole() === 1;
  }

  get canManageBatchChemicals(): boolean {
    return this.authService.getRole() === 1;
  }

  get hasActionPermission(): boolean {
    return this.canWriteBatch || this.canManageBatchChemicals;
>>>>>>> d89c627d97b7aff05863d4f6aa41fd754b888870
  }

  ngOnInit(): void {
    this.authService.ensureCurrentUser().subscribe(() => {
      this.loadFarms();
      this.loadBatches();
      this.loadCropTypes();
    });
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
        this.allBatches = batches;
        this.applyBatchFilter();
        this.isLoading = false;
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
        this.farms = this.filterFarmsByRole(farms);
        this.applyBatchFilter();
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
    if (this.isReadOnly) {
      return;
    }
    this.editingBatch = null;
    this.isFormOpen = true;
  }

  openEditForm(batch: Batch): void {
    if (this.isReadOnly || !this.canAccessBatch(batch)) {
      return;
    }
    this.editingBatch = batch;
    this.isFormOpen = true;
  }

  openDetail(batch: Batch): void {
    if (!this.canAccessBatch(batch)) {
      return;
    }

    this.viewingBatch = batch;
  }

  openQr(batch: Batch): void {
    if (!this.canAccessBatch(batch)) {
      return;
    }

    this.qrBatch = batch;
  }

  openBatchChemicals(batch: Batch): void {
    if (!this.canManageBatchChemicals || !this.canAccessBatch(batch)) {
      return;
    }

    if (!batch.crop_type_id) {
      this.showToast('Lô sản phẩm chưa có loại nông sản nên chưa thể gán hóa chất.', 'error');
      return;
    }

    this.chemicalBatch = batch;
    this.chemicals = [];
    this.batchChemicals = [];
    this.chemicalsError = '';
    this.isLoadingChemicals = true;

    forkJoin({
      chemicals: this.chemicalsService.getChemicalsByCropType(batch.crop_type_id),
      batchChemicals: this.batchesService.getBatchChemicals(batch.id),
    }).subscribe({
      next: ({ chemicals, batchChemicals }) => {
        this.chemicals = chemicals;
        this.batchChemicals = batchChemicals;
        this.isLoadingChemicals = false;
      },
      error: () => {
        this.chemicals = [];
        this.batchChemicals = [];
        this.chemicalsError = 'Không thể tải danh sách hóa chất theo loại nông sản.';
        this.isLoadingChemicals = false;
      },
    });
  }

  openDeleteConfirm(batch: Batch): void {
    if (this.isReadOnly || !this.canAccessBatch(batch)) {
      return;
    }
    this.deletingBatch = batch;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingBatch = null;
  }

  closeBatchChemicals(): void {
    this.chemicalBatch = null;
    this.chemicals = [];
    this.batchChemicals = [];
    this.chemicalsError = '';
    this.isLoadingChemicals = false;
  }

  saveBatch(value: BatchPayload): void {
<<<<<<< HEAD
    if (this.isSaving) {
      return;
    }
    this.isSaving = true;
=======
    if (this.isReadOnly) {
      return;
    }

    if (this.isFarmer && !this.farms.some((farm) => farm.id === value.farm_id)) {
      this.showToast('Bạn chỉ được tạo hoặc cập nhật lô sản phẩm thuộc nông trại của mình.', 'error');
      return;
    }

>>>>>>> d89c627d97b7aff05863d4f6aa41fd754b888870
    const isEdit = Boolean(this.editingBatch);
    const request$ = this.editingBatch
      ? this.batchesService.updateBatch(this.editingBatch.id, value)
      : this.batchesService.createBatch(value);

    request$.subscribe({
      next: () => {
        this.isSaving = false;
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật lô sản phẩm thành công.' : 'Tạo mới lô sản phẩm thành công.');
        this.loadBatches();
      },
      error: (error: HttpErrorResponse) => {
        this.isSaving = false;
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (this.isReadOnly || !this.deletingBatch) {
      return;
    }

    const productName = this.deletingBatch.product_name;
    this.batchesService.deleteBatch(this.deletingBatch.id).subscribe({
      next: () => {
        this.deletingBatch = null;
        this.showToast(`Đã xóa lô sản phẩm "${productName}".`);
        this.loadBatches();
      },
      error: () => {
        this.showToast(
          `Không thể xóa lô sản phẩm "${productName}" vì lô đã có hóa chất hoặc dữ liệu liên quan sử dụng.`,
          'error',
        );
      },
    });
  }

  saveBatchChemicals(items: BatchChemicalItem[]): void {
    if (!this.canManageBatchChemicals || !this.chemicalBatch) {
      return;
    }

    this.batchesService.setBatchChemicals(this.chemicalBatch.id, items).subscribe({
      next: () => {
        this.showToast('Cập nhật hóa chất cho lô thành công.');
        this.closeBatchChemicals();
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

  private applyBatchFilter(): void {
    this.batches = this.filterBatchesByRole(this.allBatches);
    this.currentPage = Math.min(this.currentPage, this.totalPages);
  }

  private filterFarmsByRole(farms: Farm[]): Farm[] {
    const currentUser = this.authService.getCurrentUser();
    if (!this.isFarmer || !currentUser) {
      return farms;
    }

    return farms.filter((farm) => farm.owner_id === currentUser.id);
  }

  private filterBatchesByRole(batches: Batch[]): Batch[] {
    if (!this.isFarmer) {
      return batches;
    }

    const ownedFarmIds = new Set(this.farms.map((farm) => farm.id));
    return batches.filter((batch) => ownedFarmIds.has(batch.farm_id));
  }

  private canAccessBatch(batch: Batch): boolean {
    if (!this.isFarmer) {
      return true;
    }

    return this.farms.some((farm) => farm.id === batch.farm_id);
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    return typeof detail === 'string'
      ? detail
      : 'Không thể xử lý dữ liệu lô sản phẩm. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
