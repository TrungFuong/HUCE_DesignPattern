import { Component } from '@angular/core';

@Component({
  selector: 'app-sensors-placeholder',
  standalone: true,
  template: `
    <section class="sensors-page">
      <p class="eyebrow">Cảm biến IoT</p>
      <h1>Quản lý dữ liệu cảm biến</h1>
      <p>
        Màn hình cảm biến IoT đang được phát triển. Tạm thời hệ thống đã mở menu để admin
        và nông dân có thể truy cập khi chức năng hoàn thiện.
      </p>
    </section>
  `,
  styles: [`
    :host { display: block; }
    .sensors-page {
      display: grid;
      gap: 12px;
      border: 1px solid rgba(47, 82, 53, 0.14);
      border-radius: 8px;
      padding: 28px;
      background: rgba(255, 255, 255, 0.92);
    }
    .eyebrow {
      margin: 0;
      color: #376044;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }
    h1 { margin: 0; font-size: clamp(1.8rem, 2.4vw, 2.7rem); }
    p { margin: 0; color: #4c6253; font-weight: 700; line-height: 1.6; }
  `],
})
export class SensorsPlaceholderComponent {}
