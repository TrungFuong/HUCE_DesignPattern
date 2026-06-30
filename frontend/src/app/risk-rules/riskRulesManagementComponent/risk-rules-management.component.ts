import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { CropType } from '../../crop-types/crop-type.model';
import { CropTypesService } from '../../crop-types/crop-types.service';
import { CreateUpdateRiskRulesComponent } from '../createUpdateRiskRulesComponent/create-update-risk-rules.component';
import { RiskRule, RiskRuleFormValue, RiskRulePayload } from '../risk-rule.model';
import { RiskRulesService } from '../risk-rules.service';
import { ViewDetailRiskRulesComponent } from '../viewDetailRiskRulesComponent/view-detail-risk-rules.component';

@Component({
  selector: 'app-risk-rules-management',
  standalone: true,
  imports: [CreateUpdateRiskRulesComponent, ViewDetailRiskRulesComponent],
  templateUrl: './risk-rules-management.component.html',
  styleUrls: ['./risk-rules-management.component.scss'],
})
export class RiskRulesManagementComponent implements OnInit {
  private readonly riskRulesService = inject(RiskRulesService);
  private readonly cropTypesService = inject(CropTypesService);

  currentPage = 1;
  readonly pageSize = 10;

  riskRules: RiskRule[] = [];
  cropTypes: CropType[] = [];
  editingRiskRule: RiskRule | null = null;
  viewingRiskRule: RiskRule | null = null;
  deletingRiskRule: RiskRule | null = null;
  isFormOpen = false;
  isLoading = false;
  isLoadingCropTypes = false;
  cropTypesError = '';
  toastMessage = '';
  toastType: 'success' | 'error' = 'success';

  ngOnInit(): void {
    this.loadRiskRules();
    this.loadCropTypes();
  }

  get totalPages(): number {
    return Math.max(1, Math.ceil(this.riskRules.length / this.pageSize));
  }

  get pagedRiskRules(): RiskRule[] {
    const start = (this.currentPage - 1) * this.pageSize;
    return this.riskRules.slice(start, start + this.pageSize);
  }

  get formCropTypes(): CropType[] {
    const usedCropTypeIds = new Set(
      this.riskRules
        .filter((riskRule) => riskRule.id !== this.editingRiskRule?.id)
        .map((riskRule) => riskRule.crop_type_id)
    );
    return this.cropTypes.filter((cropType) => !usedCropTypeIds.has(cropType.id));
  }

  getRowNumber(index: number): number {
    return (this.currentPage - 1) * this.pageSize + index + 1;
  }

  loadRiskRules(): void {
    this.isLoading = true;
    this.riskRulesService.getRiskRules().subscribe({
      next: (riskRules) => {
        this.riskRules = riskRules;
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
      error: (error: HttpErrorResponse) => {
        this.cropTypes = [];
        this.isLoadingCropTypes = false;
        this.cropTypesError = this.getCropTypeErrorMessage(error);
      },
    });
  }

  openCreateForm(): void {
    this.editingRiskRule = null;
    this.isFormOpen = true;
  }

  openEditForm(riskRule: RiskRule): void {
    this.editingRiskRule = riskRule;
    this.isFormOpen = true;
  }

  openDetail(riskRule: RiskRule): void {
    this.viewingRiskRule = riskRule;
  }

  openDeleteConfirm(riskRule: RiskRule): void {
    this.deletingRiskRule = riskRule;
  }

  closeForm(): void {
    this.isFormOpen = false;
    this.editingRiskRule = null;
  }

  saveRiskRule(value: RiskRuleFormValue): void {
    const request = this.editingRiskRule
      ? this.riskRulesService.updateRiskRule(this.editingRiskRule.id, this.toPayload(value))
      : this.riskRulesService.createRiskRule(this.toPayload(value));

    request.subscribe({
      next: () => {
        const isEdit = !!this.editingRiskRule;
        this.closeForm();
        this.showToast(isEdit ? 'Cập nhật mức độ rủi ro thành công.' : 'Tạo mới mức độ rủi ro thành công.');
        this.loadRiskRules();
      },
      error: (error: HttpErrorResponse) => this.showToast(this.getErrorMessage(error), 'error'),
    });
  }

  confirmDelete(): void {
    if (!this.deletingRiskRule) {
      return;
    }

    const cropTypeName = this.getCropTypeName(this.deletingRiskRule.crop_type_id);
    this.riskRulesService.deleteRiskRule(this.deletingRiskRule.id).subscribe({
      next: () => {
        this.deletingRiskRule = null;
        this.showToast(`Đã xóa mức độ rủi ro của "${cropTypeName}".`);
        this.loadRiskRules();
      },
      error: (error: HttpErrorResponse) => this.showToast(this.getErrorMessage(error), 'error'),
    });
  }

  goToPage(page: number): void {
    this.currentPage = Math.min(Math.max(page, 1), this.totalPages);
  }

  getCropTypeName(cropTypeId: string): string {
    const cropType = this.cropTypes.find((item) => item.id === cropTypeId);
    return cropType ? `${cropType.name} (${cropType.code})` : cropTypeId;
  }

  private toPayload(value: RiskRuleFormValue): RiskRulePayload {
    return {
      crop_type_id: value.crop_type_id,
      min_temperature: value.min_temperature,
      max_temperature: value.max_temperature,
      min_humidity: value.min_humidity,
      max_humidity: value.max_humidity,
      min_soil_moisture: value.min_soil_moisture,
      max_soil_moisture: value.max_soil_moisture,
      duration_minutes: value.duration_minutes,
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
      : 'Không thể xử lý dữ liệu mức độ rủi ro. Hãy kiểm tra API backend và cơ sở dữ liệu.';
  }

  private getCropTypeErrorMessage(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    return typeof detail === 'string' ? detail : 'Không thể tải danh sách loại nông sản.';
  }
}
