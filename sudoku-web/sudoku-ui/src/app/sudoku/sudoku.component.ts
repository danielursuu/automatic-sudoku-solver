import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { SudokuField } from './sudoku-field';
import { SudokuService } from '../services/sudoku.service';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-sudoku',
  templateUrl: './sudoku.component.html',
  styleUrls: ['./sudoku.component.css']
})
export class SudokuComponent implements OnInit {

  @Input()
  sudoku: number[][] = [];

  @Output()
  backToUpload = new EventEmitter<void>();

  numbers: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9];
  // imagePath: string;

  activeField: SudokuField;

  constructor(
    private readonly sudokuService: SudokuService,
    private messageService: MessageService
  ) { }

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
    this.sudokuService.sendValidatedSudokuBoard(this.sudoku).subscribe(response => {
      let board = response.body.board;

      if (JSON.stringify(this.sudoku) !== JSON.stringify(board)) {
        this.sudoku = board;
        this.messageService.add({ severity: 'success', summary: 'Sudoku Solver', detail: 'Success!' });
      } else {
        this.messageService.add({ severity: 'warn', summary: 'Sudoku Solver', detail: 'There is no solution. Please validate the grid.' });
      }
    });
  }

  onUploadClick() {
    this.sudoku = [];
    this.backToUpload.emit();
  }
}
