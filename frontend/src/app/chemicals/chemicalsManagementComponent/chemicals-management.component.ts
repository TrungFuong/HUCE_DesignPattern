import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth.service';
import { CropType } from '../../crop-types/crop-type.model';
import { CropTypesService } from '../../crop-types/crop-types.service';
import { Chemical, ChemicalPayload } from '../chemical.model';
import { ChemicalsService } from '../chemicals.service';

@Component({
  selector: 'app-chemicals-management',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './chemicals-management.component.html',
  styleUrls: ['./chemicals-management.component.scss'],
})
export class ChemicalsManagementComponent implements OnInit {
  private readonly chemicalsService = inject(ChemicalsService);
  private readonly cropTypesService = inject(CropTypesService);
  private readonly authService = inject(AuthService);

  currentPage = 1;
  readonly pageSize = 10;

  chemicals: Chemical[] = [];
  cropTypes: CropType[] = [];
  editingChemical: Chemical | null = null;
  deletingChemical: Chemical | null = null;
  isFormOpen = false;
  isLoading = false;
  isLoadingCropTypes = false;
  cropTypesError = '';
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  form: ChemicalPayload = this.createEmptyForm();

  get isReadOnly(): boolean {
    return this.authService.getRole() !== 0;
  }

  get title(): string {
    return this.editingChemical ? 'Cập nhật hóa chất' : 'Tạo hóa chất mới';
  }

  ngOnInit(): void {
    this.loadChemicals();
    this.loadCropTypes();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.chemicals.length / this.pageSize));
  }

  get pagedChemicals(): Chemical[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.chemicals.slice(start, start + this.pageSize);
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  getCropTypeName(cropTypeId: string): string {
    return this.cropTypes.find((cropType) => cropType.id === cropTypeId)?.name ?? cropTypeId;
  }

  loadChemicals(): void {
    this.isLoading = true;
    this.chemicalsService.getChemicals().subscribe({
      next: (chemicals) => {
        this.chemicals = chemicals;
        this.isLoading = false;
        this.currentPage = Math.min(this.currentPage, this.totalPages);
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.showToast(this.getErrorMessage(error), 'error');
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
    this.editingChemical = null;
    this.form = this.createEmptyForm();
    this.isFormOpen = true;
  }

  openEditForm(chemical: Chemical): void {
    if (this.isReadOnly) {
      return;
    }
    this.editingChemical = chemical;
    this.form = {
      crop_type_id: chemical.crop_type_id,
      name: chemical.name,
      unit: chemical.unit,
      description: chemical.description,
    };
    this.isFormOpen = true;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingChemical = null;
    this.form = this.createEmptyForm();
  }

  openDeleteConfirm(chemical: Chemical): void {
    if (this.isReadOnly) {
      return;
    }
    this.deletingChemical = chemical;
  }

  submitForm(): void {
    if (this.isReadOnly) {
      return;
    }

    const payload: ChemicalPayload = {
      crop_type_id: this.form.crop_type_id,
      name: this.form.name.trim(),
      unit: this.form.unit.trim(),
      description: this.form.description?.trim() || null,
    };
    const isEdit = Boolean(this.editingChemical);
    const request$ = this.editingChemical
      ? this.chemicalsService.updateChemical(this.editingChemical.id, payload)
      : this.chemicalsService.createChemical(payload);

    request$.subscribe({
      next: () => {
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật hóa chất thành công.' : 'Tạo hóa chất thành công.');
        this.loadChemicals();
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  confirmDelete(): void {
    if (this.isReadOnly || !this.deletingChemical) {
      return;
    }

    const chemicalName = this.deletingChemical.name;
    this.chemicalsService.deleteChemical(this.deletingChemical.id).subscribe({
      next: () => {
        this.deletingChemical = null;
        this.showToast(`Đã xóa hóa chất "${chemicalName}".`);
        this.loadChemicals();
      },
      error: (error: HttpErrorResponse) => {
        this.showToast(this.getErrorMessage(error), 'error');
      },
    });
  }

  goToPage(page: number): void {
    this.currentPage = Math.min(Math.max(page, 1), this.totalPages);
  }

  private createEmptyForm(): ChemicalPayload {
    return {
      crop_type_id: '',
      name: '',
      unit: '',
      description: null,
    };
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
      : 'Không thể xử lý dữ liệu hóa chất. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }
}
