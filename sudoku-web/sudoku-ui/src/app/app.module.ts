import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FileUploadModule } from 'primeng/fileupload';
import { CardModule } from 'primeng/card';

import { AppComponent } from './app.component';
import { ImageUploaderComponent } from './image-uploader/image-uploader.component';
import { GridComponent } from './sudoku/grid/grid.component';
import { SudokuComponent } from './sudoku/sudoku.component';

@NgModule({
  declarations: [
    AppComponent,
    ImageUploaderComponent,
    GridComponent,
    SudokuComponent
  ],
  imports: [
    BrowserModule,
    FileUploadModule,
    HttpClientModule,
    CardModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
