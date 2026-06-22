import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CropType } from '../../crop-types/crop-type.model';
import { RiskRule, RiskRuleFormValue } from '../risk-rule.model';

@Component({
  selector: 'app-create-update-risk-rules',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-risk-rules.component.html',
  styleUrls: ['./create-update-risk-rules.component.scss'],
})
export class CreateUpdateRiskRulesComponent implements OnChanges {
  @Input() riskRule: RiskRule | null = null;
  @Input() cropTypes: CropType[] = [];
  @Input() cropTypesError = '';
  @Input() isLoadingCropTypes = false;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<RiskRuleFormValue>();

  form: RiskRuleFormValue = this.createEmptyForm();

  get title(): string {
    return this.riskRule ? 'Cập nhật quy tắc rủi ro' : 'Tạo mới quy tắc rủi ro';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['riskRule']) {
      this.form = this.riskRule
        ? {
            crop_type_id: this.riskRule.crop_type_id,
            min_temperature: this.riskRule.min_temperature,
            max_temperature: this.riskRule.max_temperature,
            min_humidity: this.riskRule.min_humidity,
            max_humidity: this.riskRule.max_humidity,
            min_soil_moisture: this.riskRule.min_soil_moisture,
            max_soil_moisture: this.riskRule.max_soil_moisture,
            duration_minutes: this.riskRule.duration_minutes,
          }
        : this.createEmptyForm();
    }
  }

  submit(): void {
    this.save.emit({
      crop_type_id: this.form.crop_type_id,
      min_temperature: Number(this.form.min_temperature),
      max_temperature: Number(this.form.max_temperature),
      min_humidity: Number(this.form.min_humidity),
      max_humidity: Number(this.form.max_humidity),
      min_soil_moisture: this.toOptionalNumber(this.form.min_soil_moisture),
      max_soil_moisture: this.toOptionalNumber(this.form.max_soil_moisture),
      duration_minutes: Number(this.form.duration_minutes),
    });
  }

  private createEmptyForm(): RiskRuleFormValue {
    return {
      crop_type_id: '',
      min_temperature: 0,
      max_temperature: 40,
      min_humidity: 0,
      max_humidity: 100,
      min_soil_moisture: null,
      max_soil_moisture: null,
      duration_minutes: 30,
    };
  }

  private toOptionalNumber(value: number | null): number | null {
    return value === null || value === undefined || String(value) === '' ? null : Number(value);
  }
}
