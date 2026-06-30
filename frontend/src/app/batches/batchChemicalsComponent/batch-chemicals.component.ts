import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Chemical } from '../../chemicals/chemical.model';
import { Batch, BatchChemicalItem } from '../batch.model';

interface BatchChemicalFormItem {
  chemical: Chemical;
  selected: boolean;
  applied_at: string;
}

@Component({
  selector: 'app-batch-chemicals',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './batch-chemicals.component.html',
  styleUrls: ['./batch-chemicals.component.scss'],
})
export class BatchChemicalsComponent implements OnChanges {
  @Input({ required: true }) batch!: Batch;
  @Input() chemicals: Chemical[] = [];
  @Input() currentItems: BatchChemicalItem[] = [];
  @Input() isLoadingChemicals = false;
  @Input() chemicalsError = '';

  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<BatchChemicalItem[]>();

  formItems: BatchChemicalFormItem[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['chemicals'] || changes['currentItems']) {
      this.buildForm();
    }
  }

  submit(): void {
    const payload = this.formItems
      .filter((item) => item.selected)
      .map((item) => ({
        chemical_id: item.chemical.id,
        applied_at: item.applied_at ? new Date(item.applied_at).toISOString() : null,
      }));

    this.save.emit(payload);
  }

  getSelectedCount(): number {
    return this.formItems.filter((item) => item.selected).length;
  }

  private buildForm(): void {
    const existingMap = new Map(this.currentItems.map((item) => [item.chemical_id, item.applied_at]));
    this.formItems = this.chemicals.map((chemical) => {
      const appliedAt = existingMap.get(chemical.id) ?? null;
      return {
        chemical,
        selected: existingMap.has(chemical.id),
        applied_at: appliedAt ? this.toDateTimeLocalValue(appliedAt) : '',
      };
    });
  }

  private toDateTimeLocalValue(value: string): string {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return '';
    }

    const offsetMs = date.getTimezoneOffset() * 60000;
    return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16);
  }
}
