import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CropType } from '../crop-type.model';

@Component({
  selector: 'app-view-detail-crop-types',
  standalone: true,
  templateUrl: './view-detail-crop-types.component.html',
  styleUrls: ['./view-detail-crop-types.component.scss'],
})
export class ViewDetailCropTypesComponent {
  @Input({ required: true }) cropType!: CropType;
  @Output() close = new EventEmitter<void>();
}
