import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-customer-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './customer-profile.html',
  styleUrls: ['./customer-profile.css']
})
export class CustomerProfileComponent {
  
  @Input() profileData: any = null;
  @Input() nboRecommendations: string[] = [];
  
  campaignSent: boolean = false;

  onGenerateCampaign() {
    if (!this.profileData) return;

    this.campaignSent = true;
    
    setTimeout(() => {
      this.campaignSent = false;
    }, 3000);
  }
}