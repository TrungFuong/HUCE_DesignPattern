import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Batch } from '../batch.model';

@Component({
  selector: 'app-show-qr-batches',
  standalone: true,
  templateUrl: './show-qr-batches.component.html',
  styleUrls: ['./show-qr-batches.component.scss'],
})
export class ShowQrBatchesComponent {
  @Input({ required: true }) batch!: Batch;
  @Input({ required: true }) qrImageUrl = '';
  @Input({ required: true }) publicTraceUrl = '';
  @Output() close = new EventEmitter<void>();
}
