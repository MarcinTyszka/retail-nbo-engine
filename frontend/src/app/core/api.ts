import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8080/api/customers';

  constructor(private http: HttpClient) { }

  getCustomerProfile(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/${id}/profile`);
  }

  getRecommendations(basket: string[]): Observable<any> {
    return this.http.post(`${this.baseUrl}/recommendations`, basket);
  }
}