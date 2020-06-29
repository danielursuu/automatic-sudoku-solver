import { Component, OnInit, Input } from '@angular/core';

import { SudokuField } from './sudoku-field';
import { SudokuService } from '../services/sudoku.service';

@Component({
  selector: 'app-sudoku',
  templateUrl: './sudoku.component.html',
  styleUrls: ['./sudoku.component.css']
})
export class SudokuComponent implements OnInit {

  @Input()
  sudoku: number[][] = [];

  numbers: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  // imagePath: string;

  activeField: SudokuField;

  constructor(private readonly sudokuService: SudokuService) { }

  ngOnInit() {
  }

  onActiveFieldChange(event): void {
    this.activeField = event;
  }

  onClickNumber(digit: number): void {
    if (this.activeField) {
      this.sudoku[this.activeField.row][this.activeField.column] = digit;
    }
  }

  onClickValidate() {
    this.sudokuService.sendValidatedSudokuBoard(this.sudoku).subscribe(response => console.log(response));
  }
}
