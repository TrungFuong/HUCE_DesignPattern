import { Routes } from '@angular/router';
import { DashboardOverviewComponent } from './dashboard/overview/dashboard-overview.component';
import { BatchesManagementComponent } from './batches/batchesManagementComponent/batches-management.component';
import { CropTypesManagementComponent } from './crop-types/cropTypesManagementComponent/crop-types-management.component';
import { FarmsManagementComponent } from './farms/farmsManagementComponent/farms-management.component';
import { RiskRulesManagementComponent } from './risk-rules/riskRulesManagementComponent/risk-rules-management.component';
import { TraceComponent } from './trace/traceComponent/trace.component';
import { ShipmentsManagementComponent } from './shipments/shipmentsManagementComponent/shipments-management.component';
import { ContainersManagementComponent } from './containers/containersManagementComponent/containers-management.component';

export const routes: Routes = [
  { path: '', component: DashboardOverviewComponent },
  { path: 'farms', component: FarmsManagementComponent },
  { path: 'crop-types', component: CropTypesManagementComponent },
  { path: 'batches', component: BatchesManagementComponent },
  { path: 'risk-rules', component: RiskRulesManagementComponent },
  { path: 'traceability/:batch_id/public', component: TraceComponent },
  { path: 'containers', component: ContainersManagementComponent },
  { path: 'shipments', component: ShipmentsManagementComponent },
  { path: 'sensors', redirectTo: '' },
  { path: 'reports', redirectTo: '' },
  { path: '**', redirectTo: '' },
];
