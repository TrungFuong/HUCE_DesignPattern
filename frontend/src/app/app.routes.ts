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

import { authGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', component: DashboardOverviewComponent },
  { path: 'farms', component: FarmsManagementComponent, canActivate: [authGuard] },
  { path: 'crop-types', component: CropTypesManagementComponent, canActivate: [authGuard] },
  { path: 'batches', component: BatchesManagementComponent, canActivate: [authGuard] },
  { path: 'risk-rules', component: RiskRulesManagementComponent, canActivate: [authGuard] },
  { path: 'traceability/:batch_id/public', component: TraceComponent },
  { path: 'containers', component: ContainersManagementComponent, canActivate: [authGuard] },
  { path: 'shipments', component: ShipmentsManagementComponent, canActivate: [authGuard] },
  { path: 'users', component: UsersManagementComponent, canActivate: [authGuard] },
  { path: 'profile', component: ProfileComponent, canActivate: [authGuard] },
  { path: 'sensors', redirectTo: '' },
  { path: 'reports', redirectTo: '' },
  { path: '**', redirectTo: '' },
];
