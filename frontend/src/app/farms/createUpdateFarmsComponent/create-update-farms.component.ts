import { HttpErrorResponse } from '@angular/common/http';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { User } from '../../users/user.model';
import { UsersService } from '../../users/users.service';
import { Farm, FarmPayload } from '../farm.model';

@Component({
  selector: 'app-create-update-farms',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './create-update-farms.component.html',
  styleUrls: ['./create-update-farms.component.scss'],
})
export class CreateUpdateFarmsComponent implements OnChanges, OnInit {
  private readonly usersService = inject(UsersService);

  @Input() farm: Farm | null = null;
  @Output() cancel = new EventEmitter<void>();
  @Output() save = new EventEmitter<FarmPayload>();

  farmers: User[] = [];
  farmersError = '';
  isLoadingFarmers = false;
  form: FarmPayload = this.createEmptyForm();

  get title(): string {
    return this.farm ? 'Cập nhật thông tin nông trại' : 'Tạo mới nông trại';
  }

  ngOnInit(): void {
    this.loadFarmers();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['farm']) {
      this.form = this.farm
        ? {
            owner_id: this.farm.owner_id,
            name: this.farm.name,
            address: this.farm.address,
            planting_date: this.toDateInputValue(this.farm.planting_date),
            harvest_date: this.toDateInputValue(this.farm.harvest_date),
          }
        : this.createEmptyForm();
    }
  }

  submit(): void {
    this.save.emit({
      ...this.form,
      planting_date: this.form.planting_date || null,
      harvest_date: this.form.harvest_date || null,
    });
  }

  private loadFarmers(): void {
    this.isLoadingFarmers = true;
    this.farmersError = '';

    this.usersService.getFarmers().subscribe({
      next: (farmers) => {
        this.farmers = farmers.filter((farmer) => farmer.is_active);
        this.isLoadingFarmers = false;
      },
      error: (error: HttpErrorResponse) => {
        const detail = error.error?.detail;
        this.farmersError =
          typeof detail === 'string'
            ? detail
            : 'Không thể tải danh sách nông dân từ hệ thống.';
        this.isLoadingFarmers = false;
      },
    });
  }

  private createEmptyForm(): FarmPayload {
    return {
      owner_id: '',
      name: '',
      address: '',
      planting_date: null,
      harvest_date: null,
    };
  }

  private toDateInputValue(value: string | null): string | null {
    return value ? value.slice(0, 10) : null;
  }
}
