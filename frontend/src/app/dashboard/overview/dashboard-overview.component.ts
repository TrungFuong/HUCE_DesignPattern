import { DatePipe } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject } from '@angular/core';
import { forkJoin } from 'rxjs';
import { Batch } from '../../batches/batch.model';
import { BatchesService } from '../../batches/batches.service';
import { CropType } from '../../crop-types/crop-type.model';
import { CropTypesService } from '../../crop-types/crop-types.service';
import { Farm } from '../../farms/farm.model';
import { FarmsService } from '../../farms/farms.service';

interface DashboardCard {
  label: string;
  value: string;
  note: string;
}

interface StatisticRow {
  label: string;
  value: string;
  note: string;
}

interface ChartItem {
  label: string;
  value: number;
  percent: number;
}

interface FakeShipment {
  code: string;
  route: string;
  status: 'Đang giao' | 'Chờ bàn giao' | 'Hoàn tất';
  batches: number;
  progress: number;
}

@Component({
  selector: 'app-dashboard-overview',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './dashboard-overview.component.html',
  styleUrls: ['./dashboard-overview.component.scss'],
})
export class DashboardOverviewComponent implements OnInit {
  private readonly farmsService = inject(FarmsService);
  private readonly batchesService = inject(BatchesService);
  private readonly cropTypesService = inject(CropTypesService);

  farms: Farm[] = [];
  batches: Batch[] = [];
  cropTypes: CropType[] = [];
  isLoading = false;
  errorMessage = '';
  showAtRiskModal = false;
  atRiskCurrentPage = 1;
  readonly atRiskPageSize = 5;

  readonly fakeShipments: FakeShipment[] = [
    { code: 'VC-2026-001', route: 'Hà Nội -> Hải Phòng', status: 'Đang giao', batches: 4, progress: 68 },
    { code: 'VC-2026-002', route: 'Nghệ An -> Đà Nẵng', status: 'Chờ bàn giao', batches: 3, progress: 42 },
    { code: 'VC-2026-003', route: 'Lâm Đồng -> TP.HCM', status: 'Hoàn tất', batches: 6, progress: 100 },
  ];

  ngOnInit(): void {
    this.loadDashboardData();
  }

  get dashboardCards(): DashboardCard[] {
    const normalBatches = this.batches.filter((batch) => Number(batch.risk_level) === 0).length;
    const atRiskBatches = this.batches.filter((batch) => Number(batch.risk_level) === 1).length;

    return [
      {
        label: 'Tổng lô hàng',
        value: String(this.batches.length),
        note: 'Tổng số lô sản phẩm trong hệ thống',
      },
      {
        label: 'Lô bình thường',
        value: String(normalBatches),
        note: 'Lô không có cảnh báo rủi ro',
      },
      {
        label: 'Lô có rủi ro',
        value: String(atRiskBatches),
        note: 'Lô đang ở trạng thái rủi ro',
      },
      {
        label: 'Tổng nông trại',
        value: String(this.farms.length),
        note: `${this.readyForHarvestFarms} nông trại sắp thu hoạch trong 30 ngày tới`,
      },
    ];
  }

  get atRiskBatchesList(): Batch[] {
    return this.batches.filter((batch) => Number(batch.risk_level) === 1);
  }

  get atRiskTotalPages(): number {
    return Math.max(1, Math.ceil(this.atRiskBatchesList.length / this.atRiskPageSize));
  }

  get atRiskPagedBatches(): Batch[] {
    const start = (this.atRiskCurrentPage - 1) * this.atRiskPageSize;
    return this.atRiskBatchesList.slice(start, start + this.atRiskPageSize);
  }

  getFarmName(farmId: string): string {
    return this.farms.find((farm) => farm.id === farmId)?.name ?? farmId;
  }

  getCropTypeName(cropTypeId: string | null): string {
    if (!cropTypeId) return 'Không có';
    return this.cropTypes.find((c) => c.id === cropTypeId)?.name ?? cropTypeId;
  }

  openAtRiskModal(): void {
    this.showAtRiskModal = true;
    this.atRiskCurrentPage = 1;
  }

  closeAtRiskModal(): void {
    this.showAtRiskModal = false;
  }

  goToAtRiskPage(page: number): void {
    this.atRiskCurrentPage = Math.min(Math.max(page, 1), this.atRiskTotalPages);
  }

  get farmStatisticRows(): StatisticRow[] {
    const farmsWithPlantingDate = this.farms.filter((farm) => Boolean(farm.planting_date)).length;
    const farmsWithHarvestDate = this.farms.filter((farm) => Boolean(farm.harvest_date)).length;

    return [
      { label: 'Tổng nông trại', value: String(this.farms.length), note: 'Dữ liệu lấy từ API nông trại' },
      { label: 'Đã có ngày trồng', value: String(farmsWithPlantingDate), note: 'Có thể theo dõi chu kỳ sản xuất' },
      { label: 'Đã có ngày thu hoạch', value: String(farmsWithHarvestDate), note: `${this.readyForHarvestFarms} lịch gần đến hạn` },
    ];
  }

  get farmChartItems(): ChartItem[] {
    const farmsWithPlantingDate = this.farms.filter((farm) => Boolean(farm.planting_date)).length;
    const farmsWithHarvestDate = this.farms.filter((farm) => Boolean(farm.harvest_date)).length;
    const missingSchedule = Math.max(this.farms.length - farmsWithHarvestDate, 0);

    return this.toChartItems([
      { label: 'Có ngày trồng', value: farmsWithPlantingDate },
      { label: 'Có ngày thu hoạch', value: farmsWithHarvestDate },
      { label: 'Thiếu lịch thu hoạch', value: missingSchedule },
    ]);
  }

  get batchStatisticRows(): StatisticRow[] {
    const totalQuantity = this.batches.reduce((sum, batch) => sum + Number(batch.quantity || 0), 0);
    const normalBatches = this.batches.filter((batch) => Number(batch.risk_level) === 0).length;
    const atRiskBatches = this.batches.filter((batch) => Number(batch.risk_level) === 1).length;

    return [
      { label: 'Tổng lô sản phẩm', value: String(this.batches.length), note: 'Dữ liệu lấy từ API lô sản phẩm' },
      { label: 'Tổng sản lượng', value: this.formatNumber(totalQuantity), note: 'Cộng theo trường quantity' },
      { label: 'Rủi ro', value: `${atRiskBatches}/${normalBatches + atRiskBatches}`, note: 'Số lô AT_RISK trên tổng lô có phân loại' },
    ];
  }

  get batchStatusRows(): StatisticRow[] {
    return [0, 1, 2, 3].map((status) => ({
      label: this.getBatchStatusLabel(status),
      value: String(this.batches.filter((batch) => Number(batch.status) === status).length),
      note: 'Theo trạng thái xử lý lô',
    }));
  }

  get batchStatusChartItems(): ChartItem[] {
    return this.toChartItems(
      [0, 1, 2, 3].map((status) => ({
        label: this.getBatchStatusLabel(status),
        value: this.batches.filter((batch) => Number(batch.status) === status).length,
      }))
    );
  }

  get riskChartItems(): ChartItem[] {
    const normalBatches = this.batches.filter((batch) => Number(batch.risk_level) === 0).length;
    const atRiskBatches = this.batches.filter((batch) => Number(batch.risk_level) === 1).length;

    return this.toChartItems([
      { label: 'Bình thường', value: normalBatches },
      { label: 'Có rủi ro', value: atRiskBatches },
    ]);
  }

  get shipmentProgressChartItems(): ChartItem[] {
    return this.fakeShipments.map((shipment) => ({
      label: shipment.code,
      value: shipment.progress,
      percent: shipment.progress,
    }));
  }

  get shipmentStatisticRows(): StatisticRow[] {
    const totalBatches = this.fakeShipments.reduce((sum, shipment) => sum + shipment.batches, 0);
    const averageProgress = this.fakeShipments.length
      ? Math.round(this.fakeShipments.reduce((sum, shipment) => sum + shipment.progress, 0) / this.fakeShipments.length)
      : 0;

    return [
      { label: 'Chuyến mẫu', value: String(this.fakeShipments.length), note: 'Tạm dùng fake data' },
      { label: 'Lô đang vận chuyển', value: String(totalBatches), note: 'Tổng số lô trong các chuyến mẫu' },
      { label: 'Tiến độ trung bình', value: `${averageProgress}%`, note: 'Ước tính theo progress fake' },
    ];
  }

  get readyForHarvestFarms(): number {
    const today = new Date();
    const next30Days = new Date(today);
    next30Days.setDate(today.getDate() + 30);

    return this.farms.filter((farm) => {
      if (!farm.harvest_date) return false;
      const harvestDate = new Date(farm.harvest_date);
      return harvestDate >= today && harvestDate <= next30Days;
    }).length;
  }

  loadDashboardData(): void {
    this.isLoading = true;
    this.errorMessage = '';

    forkJoin({
      farms: this.farmsService.getFarms(),
      batches: this.batchesService.getBatches(),
      cropTypes: this.cropTypesService.getCropTypes(),
    }).subscribe({
      next: ({ farms, batches, cropTypes }) => {
        this.farms = farms;
        this.batches = batches;
        this.cropTypes = cropTypes;
        this.isLoading = false;
      },
      error: (error: HttpErrorResponse) => {
        this.isLoading = false;
        this.errorMessage = this.getErrorMessage(error);
      },
    });
  }

  getBatchStatusLabel(status: number): string {
    const labels: Record<number, string> = {
      0: 'Mới tạo',
      1: 'Đang vận chuyển',
      2: 'Đã giao',
      3: 'Đã đóng',
    };
    return labels[status] ?? `Trạng thái ${status}`;
  }

  private formatNumber(value: number): string {
    return new Intl.NumberFormat('vi-VN', { maximumFractionDigits: 2 }).format(value);
  }

  private toChartItems(items: Array<{ label: string; value: number }>): ChartItem[] {
    const maxValue = Math.max(...items.map((item) => item.value), 1);
    return items.map((item) => ({
      ...item,
      percent: Math.round((item.value / maxValue) * 100),
    }));
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    const detail = error.error?.detail;
    return typeof detail === 'string'
      ? detail
      : 'Không thể tải dữ liệu tổng quan. Hãy kiểm tra backend FastAPI và cơ sở dữ liệu.';
  }
}