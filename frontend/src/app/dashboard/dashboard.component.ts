import { Component, EventEmitter, Input, Output } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent {
  @Input() authMessage = '';
  @Output() logoutRequested = new EventEmitter<void>();

  readonly menuItems = [
    { path: '/', icon: '⌂', label: 'Tổng quan', exact: true },
    { path: '/farms', icon: '▦', label: 'Nông trại', exact: false },
    { path: '/crop-types', icon: '◇', label: 'Loại nông sản', exact: false },
    { path: '/batches', icon: '◫', label: 'Lô sản phẩm', exact: false },
    { path: '/risk-rules', icon: '!', label: 'Risk rule', exact: false },
    { path: '/containers', icon: '▣', label: 'Container', exact: false },
    { path: '/shipments', icon: '⇄', label: 'Vận chuyển', exact: false },
    { path: '/sensors', icon: '○', label: 'Cảm biến IoT', exact: false },
    { path: '/reports', icon: '▤', label: 'Báo cáo', exact: false },
  ];

  logout(): void {
    this.logoutRequested.emit();
  }
}
