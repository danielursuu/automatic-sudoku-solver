import { Component, EventEmitter, Input, Output } from '@angular/core';
import { SudokuField } from '../sudoku-field';

@Component({
  selector: 'grid',
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.scss']
})
export class GridComponent {
  @Input() sudoku: number[][];
  @Output() activeFieldChange = new EventEmitter<SudokuField>();

  activeField: SudokuField;

  onFieldClick(field: number, rowIndex: number, colIndex: number): void {
    this.activeField = { row: rowIndex, column: colIndex };
    this.activeFieldChange.emit(this.activeField);
  }
}
