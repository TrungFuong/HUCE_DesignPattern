import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CropType } from '../../crop-types/crop-type.model';
import { Farm } from '../../farms/farm.model';
import { Batch, BatchPayload } from '../batch.model';

@Component({
  selector: 'app-create-update-batches',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-batches.component.html',
  styleUrls: ['./create-update-batches.component.scss'],
})
export class CreateUpdateBatchesComponent implements OnChanges {
  @Input() batch: Batch | null = null;
  @Input() farms: Farm[] = [];
  @Input() farmsError = '';
  @Input() isLoadingFarms = false;
  @Input() cropTypes: CropType[] = [];
  @Input() cropTypesError = '';
  @Input() isLoadingCropTypes = false;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<BatchPayload>();

  form: BatchPayload = this.createEmptyForm();

  get title(): string {
    return this.batch ? 'Cập nhật lô sản phẩm' : 'Tạo mới lô sản phẩm';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['batch']) {
      this.form = this.batch
        ? {
            farm_id: this.batch.farm_id,
            crop_type_id: this.batch.crop_type_id,
            product_name: this.batch.product_name,
            harvest_date: this.batch.harvest_date.slice(0, 10),
            quantity: this.batch.quantity,
            quantity_unit: this.batch.quantity_unit,
            grade: this.batch.grade,
          }
        : this.createEmptyForm();
    }
  }

  submit(): void {
    this.save.emit({
      ...this.form,
      crop_type_id: this.form.crop_type_id || null,
      grade: this.form.grade?.trim() || null,
      quantity: Number(this.form.quantity),
    });
  }

  private createEmptyForm(): BatchPayload {
    return {
      farm_id: '',
      crop_type_id: null,
      product_name: '',
      harvest_date: new Date().toISOString().slice(0, 10),
      quantity: 1,
      quantity_unit: 'kg',
      grade: null,
    };
  }
}
