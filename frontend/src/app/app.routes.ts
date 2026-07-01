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
import { ChemicalsManagementComponent } from './chemicals/chemicalsManagementComponent/chemicals-management.component';

export const routes: Routes = [
<<<<<<< HEAD
  { path: '', component: DashboardOverviewComponent, title: 'Tổng quan', canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'farms', component: FarmsManagementComponent, title: 'Quản lý Nông trại', canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'crop-types', component: CropTypesManagementComponent, title: 'Quản lý Cây trồng', canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'chemicals', component: ChemicalsManagementComponent, title: 'Quản lý Vật tư', canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'batches', component: BatchesManagementComponent, title: 'Quản lý Lô sản phẩm', canActivate: [roleGuard], data: { roles: [0, 1, 2, 3] } },
  { path: 'risk-rules', component: RiskRulesManagementComponent, title: 'Quản lý Cảnh báo', canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'traceability/:batch_id/public', component: TraceComponent, title: 'Truy xuất nguồn gốc' },
  { path: 'containers', component: ContainersManagementComponent, title: 'Quản lý Kho', canActivate: [roleGuard], data: { roles: [0, 2] } },
  { path: 'shipments', component: ShipmentsManagementComponent, title: 'Quản lý Vận chuyển', canActivate: [roleGuard], data: { roles: [0, 2, 3] } },
  { path: 'users', component: UsersManagementComponent, title: 'Quản lý Người dùng', canActivate: [roleGuard], data: { roles: [0] } },
  { path: 'profile', component: ProfileComponent, title: 'Hồ sơ cá nhân', canActivate: [roleGuard], data: { roles: [0, 1, 2, 3, 4] } },
  { path: 'sensors', component: SensorsPlaceholderComponent, title: 'Cảm biến', canActivate: [roleGuard], data: { roles: [0, 1] } },
=======
  { path: '', component: DashboardOverviewComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'farms', component: FarmsManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'crop-types', component: CropTypesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'chemicals', component: ChemicalsManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'batches', component: BatchesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1, 2] } },
  { path: 'risk-rules', component: RiskRulesManagementComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
  { path: 'traceability/:batch_id/public', component: TraceComponent },
  { path: 'containers', component: ContainersManagementComponent, canActivate: [roleGuard], data: { roles: [0, 2] } },
  { path: 'shipments', component: ShipmentsManagementComponent, canActivate: [roleGuard], data: { roles: [0, 2, 3] } },
  { path: 'users', component: UsersManagementComponent, canActivate: [roleGuard], data: { roles: [0] } },
  { path: 'profile', component: ProfileComponent, canActivate: [roleGuard], data: { roles: [0, 1, 2, 3, 4] } },
  { path: 'sensors', component: SensorsPlaceholderComponent, canActivate: [roleGuard], data: { roles: [0, 1] } },
>>>>>>> e29208936fe833c1dab2397a507e52f43d495de7
  { path: 'reports', redirectTo: '' },
  { path: '**', redirectTo: '' },
];
