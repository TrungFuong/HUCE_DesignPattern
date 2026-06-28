import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { RiskRule, RiskRulePayload } from './risk-rule.model';

@Injectable({ providedIn: 'root' })
export class RiskRulesService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = 'http://localhost:8000';

  getRiskRules(): Observable<RiskRule[]> {
    return this.http.get<RiskRule[]>(`${this.apiBaseUrl}/risk-rules/`);
  }

  getRiskRule(id: string): Observable<RiskRule> {
    return this.http.get<RiskRule>(`${this.apiBaseUrl}/risk-rules/id/${id}`);
  }

  createRiskRule(payload: RiskRulePayload): Observable<RiskRule> {
    return this.http.post<RiskRule>(`${this.apiBaseUrl}/risk-rules/`, payload);
  }

  updateRiskRule(id: string, payload: RiskRulePayload): Observable<RiskRule> {
    return this.http.put<RiskRule>(`${this.apiBaseUrl}/risk-rules/id/${id}`, payload);
  }

  deleteRiskRule(id: string): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${this.apiBaseUrl}/risk-rules/id/${id}`);
  }
}
