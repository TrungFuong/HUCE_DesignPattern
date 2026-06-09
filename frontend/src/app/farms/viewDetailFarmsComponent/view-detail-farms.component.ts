import { DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Farm } from '../farm.model';

@Component({
  selector: 'app-view-detail-farms',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './view-detail-farms.component.html',
  styleUrls: ['./view-detail-farms.component.scss'],
})
export class ViewDetailFarmsComponent {
  @Input({ required: true }) farm!: Farm;
  @Input() ownerName = '';
  @Output() close = new EventEmitter<void>();
}
