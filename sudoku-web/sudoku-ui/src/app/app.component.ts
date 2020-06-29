import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  uploadEnabled: boolean = true;
  validatorEnabled: boolean = false;

  sudokuForValidation: number[][] = [];

  onUploaded(event) {
    this.uploadEnabled = false;
    this.validatorEnabled = true;
    this.sudokuForValidation = event.board;
  }
}
