import { DatePipe, DecimalPipe, SlicePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TraceResponse, TraceSensorLog, TraceShipment } from '../trace.model';
import { TraceService } from '../trace.service';

@Component({
  selector: 'app-trace',
  standalone: true,
  imports: [DatePipe, DecimalPipe, SlicePipe],
  templateUrl: './trace.component.html',
  styleUrls: ['./trace.component.scss'],
})
export class TraceComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly traceService = inject(TraceService);

  batchId = '';
  data: TraceResponse | null = null;
  isLoading = false;
  errorMessage = '';

  ngOnInit(): void {
    this.batchId = this.route.snapshot.paramMap.get('batch_id') ?? '';
    if (this.batchId) {
      this.loadTrace();
    } else {
      this.errorMessage = 'Không tìm thấy mã lô hàng trong URL.';
    }
  }

  loadTrace(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.traceService.getBlockchainHash(this.batchId).subscribe({
      next: (res) => console.log('Blockchain hash called:', res),
      error: (err) => console.error('Blockchain hash call failed:', err)
    });

    this.traceService.getPublicTrace(this.batchId).subscribe({
      next: (data) => {
        this.data = data;
        this.isLoading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.isLoading = false;
        this.errorMessage =
          err.status === 404
            ? 'Không tìm thấy lô hàng. Mã QR có thể không hợp lệ hoặc lô hàng đã bị xóa.'
            : 'Không thể tải thông tin lô hàng. Hãy kiểm tra kết nối và thử lại.';
      },
    });
  }

  /* ── helpers ── */

  get statusLabel(): string {
    return this.mapStatus(this.data?.product?.status ?? '');
  }
  get riskLabel(): string {
  return this.data?.product?.risk_level === 'AT_RISK' ? 'Có rủi ro' : 'Bình thường';
  }

  get statusClass(): string {
    const s = this.data?.product?.status ?? '';
    if (s === 'DELIVERED' ) return 'status-ok';
    if (s === 'IN_TRANSIT') return 'status-transit';
    return 'status-neutral';
  }

  get isVerified(): boolean {
    return this.data?.verification?.is_verified ?? false;
  }

  get journeySteps(): { label: string; done: boolean; active: boolean }[] {
  const status = this.data?.product?.status ?? '';
  const order = ['CREATED', 'IN_TRANSIT', 'DELIVERED'];
  const labels = ['Chờ xác nhận', 'Đang giao', 'Đã giao'];
  const idx = order.indexOf(status);
    return labels.map((label, i) => ({
      label,
      done: i < idx,
      active: i === idx,
    }));
  }

  get primaryShipment(): TraceShipment | null {
    return this.data?.shipments?.[0] ?? null;
  }

  get tempLogs(): TraceSensorLog[] {
    return (this.data?.sensor_logs ?? []).filter((l) => l.temperature !== null);
  }

  get humidityLogs(): TraceSensorLog[] {
    return (this.data?.sensor_logs ?? []).filter((l) => l.humidity !== null);
  }
    get soilMoistureLogs(): TraceSensorLog[] {
    return (this.data?.sensor_logs ?? []).filter((l) => l.soil_moisture !== null);
  }

  get latestSoilMoisture(): number | null {
    const logs = this.soilMoistureLogs;
    return logs.length ? logs[logs.length - 1].soil_moisture : null;
  }

  get avgTemp(): number | null {
    const vals = this.tempLogs.map((l) => l.temperature as number);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  }

  get avgHumidity(): number | null {
    const vals = this.humidityLogs.map((l) => l.humidity as number);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  }

  get avgSoilMoisture(): number | null {
    const vals = this.soilMoistureLogs.map((l) => l.soil_moisture as number);
    return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
  }

  get sensorSparkSoilMoisture(): string {
    return this.buildSparkline(
      this.soilMoistureLogs.map((l) => l.soil_moisture as number),
      36
    );
  }

  get latestTemp(): number | null {
    const logs = this.tempLogs;
    return logs.length ? logs[logs.length - 1].temperature : null;
  }

  get latestHumidity(): number | null {
    const logs = this.humidityLogs;
    return logs.length ? logs[logs.length - 1].humidity : null;
  }

  get hasRiskViolation(): boolean {
    return this.data?.product?.risk_level === 'AT_RISK';
  }

  get sensorSparkTemperature(): string {
    return this.buildSparkline(this.tempLogs.map((l) => l.temperature as number), 36);
  }

  get sensorSparkHumidity(): string {
    return this.buildSparkline(this.humidityLogs.map((l) => l.humidity as number), 36);
  }

  buildSparkline(values: number[], height: number): string {
    if (values.length < 2) return '';
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min || 1;
    const w = 100;
    const step = w / (values.length - 1);
    return values
      .map((v, i) => {
        const x = +(i * step).toFixed(1);
        const y = +(height - ((v - min) / range) * (height - 6) - 3).toFixed(1);
        return `${i === 0 ? 'M' : 'L'}${x},${y}`;
      })
      .join(' ');
  }

  mapStatus(s: string): string {
    const map: Record<string, string> = {
      CREATED: 'Chờ xác nhận',
      IN_TRANSIT: 'Đang giao',
      DELIVERED: 'Đã giao',
    };
    return map[s] ?? s;
  }

  mapShipmentStatus(s: string): string {
    const map: Record<string, string> = {
      CREATED: 'Mới tạo',
      IN_TRANSIT: 'Đang vận chuyển',
      DELIVERED: 'Đã giao',
      CANCELLED: 'Đã hủy',
    };
    return map[s] ?? s;
  }

  shortHash(h: string | null | undefined, len = 20): string {
    if (!h) return '—';
    return h.length > len ? h.slice(0, len) + '…' : h;
  }

  get blockchainUrl(): string {
    return `http://localhost:8000/blockchain/hash/${this.batchId}`;
  }

  get qrCodeUrl(): string {
    const data = encodeURIComponent(this.blockchainUrl);
    return `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${data}`;
  }
}