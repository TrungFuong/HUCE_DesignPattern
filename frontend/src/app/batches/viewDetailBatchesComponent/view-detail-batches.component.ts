import { DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Batch } from '../batch.model';

@Component({
  selector: 'app-view-detail-batches',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './view-detail-batches.component.html',
  styleUrls: ['./view-detail-batches.component.scss'],
})
export class ViewDetailBatchesComponent {
  @Input({ required: true }) batch!: Batch;
  @Input() farmName = '';
  @Input() cropTypeName = '';
  @Output() close = new EventEmitter<void>();
}
