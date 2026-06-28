import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RiskRule } from '../risk-rule.model';

@Component({
  selector: 'app-view-detail-risk-rules',
  standalone: true,
  templateUrl: './view-detail-risk-rules.component.html',
  styleUrls: ['./view-detail-risk-rules.component.scss'],
})
export class ViewDetailRiskRulesComponent {
  @Input({ required: true }) riskRule!: RiskRule;
  @Input() cropTypeName = '';
  @Output() close = new EventEmitter<void>();
}
