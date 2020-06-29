import { Injectable } from '@angular/core';
import { ApiCallerService } from '../shared/services/api-caller.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SudokuService {

  constructor(private readonly apiCaller: ApiCallerService) { }

  sendValidatedSudokuBoard(board: number[][]): Observable<any> {
    return this.apiCaller.post('/validate', board);
  }
}
