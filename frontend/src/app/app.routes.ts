import { Routes } from '@angular/router';
import { DashboardOverviewComponent } from './dashboard/overview/dashboard-overview.component';
import { BatchesManagementComponent } from './batches/batchesManagementComponent/batches-management.component';
import { CropTypesManagementComponent } from './crop-types/cropTypesManagementComponent/crop-types-management.component';
import { FarmsManagementComponent } from './farms/farmsManagementComponent/farms-management.component';
import { RiskRulesManagementComponent } from './risk-rules/riskRulesManagementComponent/risk-rules-management.component';
import { TraceComponent } from './trace/traceComponent/trace.component';
import { ShipmentsManagementComponent } from './shipments/shipmentsManagementComponent/shipments-management.component';
import { ContainersManagementComponent } from './containers/containersManagementComponent/containers-management.component';
import { UsersManagementComponent } from './users/usersManagementComponent/users-management.component';
import { ProfileComponent } from './profile/profileComponent/profile.component';
import { SensorsPlaceholderComponent } from './sensors/sensors-placeholder.component';
import { roleGuard } from './role.guard';

export const routes: Routes = [
  { path: '', component: DashboardOverviewComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'farms', component: FarmsManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'crop-types', component: CropTypesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'batches', component: BatchesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1, 2] } },
  { path: 'risk-rules', component: RiskRulesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'traceability/:batch_id/public', component: TraceComponent },
  { path: 'containers', component: ContainersManagementComponent, canActivate: [roleGuard], data: { roles: [0, 2] } },
  { path: 'shipments', component: ShipmentsManagementComponent, canActivate: [roleGuard], data: { roles: [0, 2, 3] } },
  { path: 'users', component: UsersManagementComponent, canActivate: [roleGuard], data: { roles: [0] } },
  { path: 'profile', component: ProfileComponent, canActivate: [roleGuard], data: { roles: [0, 1, 2, 3] } },
  { path: 'sensors', component: SensorsPlaceholderComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'reports', redirectTo: '' },
  { path: '**', redirectTo: '' },
];
