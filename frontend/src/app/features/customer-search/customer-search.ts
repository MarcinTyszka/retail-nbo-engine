import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api';
import { CustomerProfileComponent } from '../customer-profile/customer-profile';

@Component({
  selector: 'app-customer-search',
  standalone: true,
  imports: [CommonModule, FormsModule, CustomerProfileComponent],
  templateUrl: './customer-search.html',
  styleUrls: ['./customer-search.css']
})
export class CustomerSearchComponent {
  
  searchId: number | null = null;
  customerProfile: any = null;
  currentBasket: string[] = []
  recommendations: string[] = [];
  errorMessage: string = '';

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

onSearch() {
    if (!this.searchId) return;
    this.resetState();

    this.apiService.getCustomerProfile(this.searchId).subscribe({
      next: (data) => {
        this.customerProfile = data;
        this.currentBasket = data.currentBasket || [];
        this.recommendations = data.recommendations || [];
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.errorMessage = 'Customer not found or server error occurred.';
        console.error(err);
        this.cdr.detectChanges();
      }
    });
  }

  private resetState() {
    this.errorMessage = '';
    this.customerProfile = null;
    this.currentBasket = [];
    this.recommendations = [];
    this.cdr.detectChanges();
  }

  fetchRecommendations(basket: string[]) {
    this.apiService.getRecommendations(basket).subscribe({
      next: (data) => {
        this.recommendations = data.recommendations || [];
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error(err);
        this.cdr.detectChanges();
      }
    });
  }


}