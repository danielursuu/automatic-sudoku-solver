import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  uploadEnabled: boolean = true;
  validatorEnabled: boolean = false;

  sudoku: { board: number[][], fileName: string };

  onUploaded(event) {
    this.uploadEnabled = false;
    this.validatorEnabled = true;
    this.sudoku = event;
  }

  onBackToUpload() {
    this.uploadEnabled = true;
    this.validatorEnabled = false;
  }
}
