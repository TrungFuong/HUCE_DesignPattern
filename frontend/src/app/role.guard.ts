import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { map } from 'rxjs';
import { AuthService } from './auth.service';

export const defaultPathForRole = (role: number | null): string => {
  if (role === 2) {
    return '/batches';
  }
  if (role === 3) {
    return '/shipments';
  }
  if (role === 4) {
    return '/profile';
  }
  return '/';
};

export const roleGuard: CanActivateFn = (route) => {
  const authService = inject(AuthService);
  const router = inject(Router);
  const allowedRoles = (route.data?.['roles'] as number[] | undefined) ?? [];

  return authService.ensureCurrentUser().pipe(
    map((user) => {
      if (!user) {
        return false;
      }
      if (!allowedRoles.length || allowedRoles.includes(user.role)) {
        return true;
      }
      return router.createUrlTree([defaultPathForRole(user.role)]);
    }),
  );
};
