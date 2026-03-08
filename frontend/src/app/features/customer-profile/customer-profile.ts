import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-customer-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './customer-profile.html',
  styleUrls: ['./customer-profile.css']
})
export class CustomerProfileComponent implements OnChanges {
  
  @Input() profileData: any = null;
  @Input() currentBasket: string[] = [];
  @Input() nboRecommendations: string[] = [];
  
  campaignSent: boolean = false;
  segmentName: string = '';
  segmentDescription: string = '';

  ngOnChanges(changes: SimpleChanges) {
    // Reacts to incoming data and translates raw cluster ID to business persona
    if (changes['profileData'] && this.profileData) {
      this.mapClusterToPersona(this.profileData.segment);
    }
  }

  private mapClusterToPersona(clusterId: number) {
    // Maps K-Means integer output to human-readable marketing segments
    switch (clusterId) {
      case 0:
        this.segmentName = 'Bargain Hunters';
        this.segmentDescription = 'Highly responsive to discounts, low average order value.';
        break;
      case 1:
        this.segmentName = 'Loyal Big Spenders';
        this.segmentDescription = 'High frequency and monetary value. VIP treatment required.';
        break;
      case 2:
        this.segmentName = 'Churn Risk';
        this.segmentDescription = 'Used to buy frequently, but hasn\'t visited recently.';
        break;
      default:
        this.segmentName = 'Regular Customers';
        this.segmentDescription = 'Average spending and frequency. Steady revenue stream.';
    }
  }

  onGenerateCampaign() {
    if (!this.profileData) return;
    this.campaignSent = true;
    setTimeout(() => {
      this.campaignSent = false;
    }, 3000);
  }
}