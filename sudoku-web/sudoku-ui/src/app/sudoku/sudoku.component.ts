import { Component, OnInit } from '@angular/core';

import { SudokuField } from './sudoku-field';

@Component({
  selector: 'app-sudoku',
  templateUrl: './sudoku.component.html',
  styleUrls: ['./sudoku.component.css']
})
export class SudokuComponent implements OnInit {
  sudoku: number[][];
  numbers: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9];

  activeField: SudokuField;

  constructor() { }

  ngOnInit() {
    this.prepareSudokuGrid();
  }

  private prepareSudokuGrid(): void {
    this.sudoku = [
      [0, 0, 0, 6, 0, 4, 7, 0, 0],
      [7, 0, 6, 0, 0, 0, 0, 0, 9],
      [0, 0, 0, 0, 0, 5, 0, 8, 0],
      [0, 7, 0, 0, 2, 0, 0, 9, 3],
      [8, 0, 0, 0, 0, 0, 0, 0, 5],
      [4, 3, 0, 0, 1, 0, 0, 7, 0],
      [0, 5, 0, 2, 0, 0, 0, 0, 0],
      [3, 0, 0, 0, 0, 0, 2, 0, 8],
      [0, 0, 2, 3, 0, 1, 0, 0, 0]
    ];
  }

  onActiveFieldChange(event): void {
    this.activeField = event;
  }

  onClickNumber(digit: number): void {
    if (this.activeField) {
      this.sudoku[this.activeField.row][this.activeField.column] = digit;
    }
  }
}
