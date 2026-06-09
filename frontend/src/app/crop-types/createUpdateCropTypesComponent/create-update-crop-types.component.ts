import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CropType, CropTypePayload } from '../crop-type.model';

@Component({
  selector: 'app-create-update-crop-types',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-crop-types.component.html',
  styleUrls: ['./create-update-crop-types.component.scss'],
})
export class CreateUpdateCropTypesComponent implements OnChanges {
  @Input() cropType: CropType | null = null;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<CropTypePayload>();

  form: CropTypePayload = this.createEmptyForm();

  get title(): string {
    return this.cropType ? 'Cập nhật loại nông sản' : 'Tạo mới loại nông sản';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['cropType']) {
      this.form = this.cropType
        ? {
            code: this.cropType.code,
            name: this.cropType.name,
            description: this.cropType.description,
          }
        : this.createEmptyForm();
    }
  }

  submit(): void {
    this.save.emit({
      code: this.form.code.trim().toUpperCase(),
      name: this.form.name.trim(),
      description: this.form.description?.trim() || null,
    });
  }

  private createEmptyForm(): CropTypePayload {
    return {
      code: '',
      name: '',
      description: null,
    };
  }
}
