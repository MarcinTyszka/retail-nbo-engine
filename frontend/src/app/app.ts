import { Component } from '@angular/core';
import { CustomerSearchComponent } from './features/customer-search/customer-search';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CustomerSearchComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  title = 'frontend';
}