import { Component } from '@angular/core';

@Component({
  selector: 'app-sensors-placeholder',
  standalone: true,
  template: `
    <section class="placeholder-page">
      <p class="eyebrow">Cảm biến IoT</p>
      <h1>Quản lý dữ liệu cảm biến</h1>
      <div class="placeholder-card">
        <span class="sensor-icon" aria-hidden="true">◉</span>
        <div>
          <h2>Chức năng đang được phát triển</h2>
          <p>
            Màn hình theo dõi nhiệt độ, độ ẩm và độ ẩm đất sẽ được bổ sung trong
            phiên bản tiếp theo.
          </p>
        </div>
      </div>
    </section>
  `,
  styleUrls: ['./sensors-placeholder.component.scss'],
})
export class SensorsPlaceholderComponent {}
