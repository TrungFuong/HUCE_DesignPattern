import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { User } from '../../users/user.model';
import { Farm, FarmPayload } from '../farm.model';

@Component({
  selector: 'app-create-update-farms',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-farms.component.html',
  styleUrls: ['./create-update-farms.component.scss'],
})
export class CreateUpdateFarmsComponent implements OnChanges {
  @Input() farm: Farm | null = null;
  @Input() farmers: User[] = [];
  @Input() ownerLocked = false;
  @Input() farmersError = '';
  @Input() isLoadingFarmers = false;
  @Input() isSaving = false;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<FarmPayload>();

  form: FarmPayload = this.createEmptyForm();

  get title(): string {
    return this.farm ? 'Cập nhật thông tin nông trại' : 'Tạo mới nông trại';
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['farm'] || changes['farmers'] || changes['ownerLocked']) {
      this.form = this.farm
        ? {
            owner_id: this.farm.owner_id,
            name: this.farm.name,
            address: this.farm.address,
            planting_date: this.toDateInputValue(this.farm.planting_date),
            harvest_date: this.toDateInputValue(this.farm.harvest_date),
          }
        : {
            ...this.createEmptyForm(),
            owner_id: this.ownerLocked && this.farmers.length ? this.farmers[0].id : '',
          };
    }
  }

  submit(): void {
    if (this.isSaving) {
      return;
    }
    this.save.emit({
      ...this.form,
      planting_date: this.form.planting_date || null,
      harvest_date: this.form.harvest_date || null,
    });
  }

  private createEmptyForm(): FarmPayload {
    return {
      owner_id: '',
      name: '',
      address: '',
      planting_date: null,
      harvest_date: null,
    };
  }

  private toDateInputValue(value: string | null): string | null {
    return value ? value.slice(0, 10) : null;
  }
}
